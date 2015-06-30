import sys
import traceback
import string
from struct import *
from socket import *
from global_value import *

from registered_controller import *
from hp_api.hp_controller_api import *
from hp_api.hp_result_print import *
from hp_api.config_hp_cmd import *
from hp_api.config_hp_switch_cmd import *

mac_db = {}
sw_alias_db = {}
g_controller_uid = str()

allchars = "".join(chr(a) for a in range(256))
delchars = set(allchars) - set(string.hexdigits)

def checkmac(s):
    mac = s.translate("".join(allchars),"".join(delchars))
    if len(mac) != 12:
        raise ValueError, "Ethernet MACs are always 12 hex characters, you entered %s" % mac 
    return mac.upper()

def ip_check(ip_addr):
	try:
		ip_packed = inet_aton(ip_addr)
		ip = unpack("!L", ip_packed)[0]
	except Exception:
		print "IP Error"
		traceback.print_exc()
		return None
	return ip 

def config_json_read(file_path):
	try:
		with open(file_path,"r") as read_file:
			json_data = json.load(read_file)
			read_file.close()
	except Exception:
		traceback.print_exc()
		return None 

	return json_data

def config_json_write(file_path, json_data):
	try :
		with open(file_path,"w+") as write_file:
			json.dump(json_data, write_file)
			write_file.close()
	except Exception:
		traceback.print_exc()

	return None 

def config_json_search_entry(json_data, entry):
	return None

def port_check(port):
	if port <= 65535 and port >= 0: 
		return port 
	else:
		print "Port range over"
		return None 

def search_controller(json_data, controller_uid):
	for controller_componet in json_data:
		if controller_componet['uid'] == controller_uid:
			print "serach controller_uid!!"
			#return index json_data
			return controller_componet
	return False 

def search_swirch(json_data, switch_mac, switch_dpid):
	for switch_componet in json_data:
		print "switch_componet",switch_componet
		if switch_componet['mac'] == switch_mac and switch_componet['dpid'] == switch_dpid:
			print switch_componet
			return switch_componet

	return False

def controller_all_config(ip, port, token):
	dpid_db = []
	port_mac = [] 
	#print ip, port, token
	try:
		stats_response = hp_api_stats(ip, port, token, 0)
		controller_uid = stats_response['controller_stats'][0]['uid']
		response = hp_api_ports(ip, port, token, 0)
		version_response = hp_api_version(ip, port, token, 0)
		dpid_res = hp_api_get_datapaths(ip, port, token)

		datapath_count = len(dpid_res['datapaths'])
		for x in range(datapath_count):
			port_mac = []
			tmp_dpids = json.dumps(dpid_res['datapaths'][x]['dpid'])
			port_res = hp_api_get_datapath_port(ip, port, token, tmp_dpids, 0)
			dpids.append(tmp_dpids)

			for y in range(len(port_res['ports'])):
				mac_alias = {port_res['ports'][y]['mac'] : None }
				port_mac.append(mac_alias)

			mac_db[tmp_dpids.split('"')[1]] = port_mac
			#hp_api_get_datapath_flows(token, tmp_dpids)

		return controller_uid
	except Exception:
		traceback.print_exc()

	return None 

def refresh_controller_switch_alias(ip, port, token):
	mac_db = {}
	sw_alias_db = {}
	controller_uid = controller_all_config(ip, port, token)
	return controller_uid

def compare_and_update_alias(org_switch_alias):
	for org_dpid in org_switch_alias:
		for port_count in range(len(org_dpid['ports'])):
			try :
				dpid = org_dpid['dpid']
				sw_alias = org_dpid['sw_alias']
				org_mac = org_dpid['ports'][port_count]['mac']
				# search mac_db
				search_list = {org_mac:None}
				# update index mac_db search 
				index = mac_db[dpid].index(search_list)
				# org db -> mac_db alias update 
				s_port_alias = org_dpid['ports'][port_count]['port_alias'] 
				mac_db[dpid][index][org_mac] = s_port_alias
				sw_alias_db[dpid] = sw_alias

			except Exception:
				traceback.print_exc()
				print "pass"
				pass
def default_sw_alias_db():
	for datapath in mac_db.keys():
		sw_alias_db[datapath] = "".join(datapath.split(":"))

def make_alias_json(controller_uid, con_alias):
	json_dpid_alias = []
	for datapath in mac_db.keys():
		json_port_alias = []
		#print org_json_alias['controllers']['switchs'].index(datapath)
		for x in mac_db[datapath]:
			mac = x.keys()[0]
			s_port_alias = x[mac]
			json_port_alias.append({"mac":str(x.keys()[0]), "port_alias":s_port_alias})
		try:
			sw_alias = sw_alias_db[datapath]
		except Exception:
			sw_alias = "".join(datapath.split(":"))
			traceback.print_exc()
		json_dpid_alias.append({"dpid":datapath,"sw_alias":sw_alias,"ports":json_port_alias})

	update_alias_json = {"controllers":{
		"con_alias": con_alias,
		"c_uid":controller_uid,
		"switchs":json_dpid_alias
		}
		}
	return update_alias_json

def refresh_alias_json_db(ip, port, token, user, password):
	json_dpid_alias = []
	if token == None:
		tmp_token = hp_api_login(ip, port, user, password)
		token = tmp_token['token']	

	controller_uid = refresh_controller_switch_alias(ip, port, token)
	
	sw_alias_string = str()
	dpid_string = str()
	file_path = CONF_PATH+"/"+controller_uid+".json"

	org_json_alias = config_json_read(file_path)
	if org_json_alias == None:
		con_alias = None 
		update_alias_json = make_alias_json(controller_uid, con_alias)
		default_sw_alias_db()
	else :
		con_alias = org_json_alias['controllers']['con_alias']
		org_switch_alias = org_json_alias['controllers']['switchs']
		compare_and_update_alias(org_switch_alias)
		update_alias_json = make_alias_json(controller_uid, con_alias)

	config_json_write(file_path, update_alias_json)
	
	return controller_uid

if __name__ == "__main__":
	ip = "192.168.101.76"
	port = 8443
	user = "sdn"
	password = "skyline"
	refresh_alias_json_db(ip, port, None, user, password)
