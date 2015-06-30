import httplib
import logging
import json
import copy
import global_value
import utils 
from _socket import timeout
debug = True
# debug = False
# Global variable
HTTP_REQUEST_TIMEOUT = 5
LOG_PATH = "test.log"

import logging
logger = logging.getLogger('root')
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)
if debug:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

def find_alias_in_dpid(dpid, sw_alias_db):
    for alias, alias_dpid in sw_alias_db.iteritems():
        if alias_dpid == dpid:
            return alias
    return None

def controller_db_init(ip, port, token):
    file_path = global_value.CONF_PATH +"/"+ ip + ".json"
    # logger.debug(file_path)
    import os.path
    controller_db = dict()
  
    if os.path.isfile(file_path):
        controller_db = utils.config_json_read(file_path)
    if controller_db == None or len(controller_db) == 0:
        open_flie = open(file_path, "a+")
        controller_db = {
            "ip"        :   ip,
            "con_alias" :   ip,
            "sw_alias"  :   {}
        }
    controller_db["sw_alias"] = set_sw_alias(ip, port, token, controller_db.get("sw_alias"))
    utils.config_json_write(file_path, controller_db)
    return controller_db

def set_sw_alias(ip, port, token, sw_alias_db):
    switch_list = get_switch_list(ip, port, token)
    sw_alias = dict()
    if switch_list == None:
        print "fail to get switch list"
        return sw_alias_db
    for switch in switch_list:
        sw_alias[switch["id"]] = switch["id"]

    if len(sw_alias_db) > 0:
        for alias, dpid in sw_alias_db.iteritems():
            if dpid in sw_alias.keys():
                sw_alias.pop(dpid)
            sw_alias[alias] = dpid

    return sw_alias

def login(ip, port, username, password):
    uri_login = "/oauth2/token"
    # logger.debug("login")
    params = get_encoded_login_params(username, password)
    header = {
        "Content-type":"application/x-www-form-urlencoded",
        "Accept":"application/json"
    }
    connection = httplib.HTTPConnection(ip, int(port), timeout=HTTP_REQUEST_TIMEOUT)
    # msg = connection.host, connection.port
    # logger.debug(msg)
    response = None
    try :
        connection.request("POST", uri_login, body=params, headers=header)
        response = connection.getresponse()
        # logger.debug(response.getheaders())
        if response.status != 201 :
            print "login fail"
            # logger.info("http status : "+ str(response.status))
            # logger.info("reason : "+ str(response.reason))
            return None
    except timeout:
        print "error : request timeout"
        return None
        

    response_body = json.loads(response.read())
    token_type = response_body["token_type"]
    access_token = response_body["access_token"]
    token = token_type + " " + access_token

    return token

def get_encoded_login_params(username, password):
    import urllib
    params = {
        "scope" : "sdn",
        "grant_type" : "password",
        "username" : username,
        "password" : password
    }

    encoded_params = urllib.urlencode(params)
    
    return encoded_params


def get_response(ip, port, token, uri, method, body):
    # logger.debug(token)
    connection = httplib.HTTPConnection(ip, int(port), timeout=HTTP_REQUEST_TIMEOUT)
    header = {
        "Accept" : "application/json",
        "Authorization" : token,
        "Content-Type" : "application/json"
    }
    try :
        connection.request(method, uri, body, header)
        response = connection.getresponse()
        if response.status != 200:
            # logger.debug(response.read())
            print "http status : ", response.status, response.reason
            return None
    except timeout:
        print "error : request timeout"
        return None

    return response

def get_switch_list(ip, port, token):
    uri_get_switch_list = "/restconf/operational/opendaylight-inventory:nodes/"
    response = get_response(ip, port, token, uri_get_switch_list, "GET", "")
    if response == None:
        return None

    # Converting response to json_dict
    json_dict = json.loads(response.read())
    switches = list()
    if len(json_dict['nodes']) == 0 :
        print "not attached switch"
    else : 
        switches = json_dict['nodes']['node']

	return switches

def get_switch(ip, port, token, dpid):
    uri_get_switch = "/restconf/operational/opendaylight-inventory:nodes/node/" + dpid + "/"
    response = get_response(ip, port, token, uri_get_switch, "GET", "")
    if response == None:
        print "switch info not found"
        return None
   
    json_dict = json.loads(response.read())
    switch = json_dict["node"][0]
    return switch

def get_topology_list(ip, port, token):
    uri_get_topology_list = "/restconf/operational/network-topology:network-topology/"
    response = get_response(ip, port, token, uri_get_topology_list, "GET", "")
    if response == None:
        return None

    # Converting response to json_dict
    json_dict = json.loads(response.read())
    topology_list = list()
    if len(json_dict['network-topology']['topology']) == 0 :
        print "not attached topology"
    else : 
        topology_list = json_dict['network-topology']['topology']

	return topology_list

def get_topology(ip, port, topology_id):
    uri_get_topology = "/restconf/operational/network-topology:network-topology/" + topology_id + "/"
    response = get_response(ip, port, token , uri_get_topology ,"GET", "")
    if response == None:
        return None

    json_dict = json.loads(response.read())
    topology = json_dict["topology"][0]
    return topology

def get_host(ip, port, token, host_id):
    topology_list = get_topology_list(ip, port, token)
    if topology_list == None:
        return None
    for topology in topology_list:
        node_list = topology["node"]
        for node in node_list:
            if node.get("node-id") == host_id:
                return node
    print "host id not found"
    return None

def get_switch_port_list(ip, port, token, dpid):
    uri_get_switch = "/restconf/operational/opendaylight-inventory:nodes/node/" + dpid + "/"
    response = get_response(ip, port, token, uri_get_switch, "GET", "")
    if response == None:
        return None

    json_dict = json.loads(response.read())
    switch_port_list = json_dict["node"][0]["node-connector"]
    return switch_port_list

def get_switch_port(ip, port, token, dpid, switch_port_id):
    uri_get_switch_port = "/restconf/operational/opendaylight-inventory:nodes/node/" + dpid + "/node-connector/" + switch_port_id + "/"
    response = get_response(ip, port, token, uri_get_switch_port, "GET", "")
    if response == None:
        return None
    
    json_dict = json.loads(response.read())
    switch_port = json_dict["node-connector"][0]
    return switch_port

def get_switch_flow_list(ip, port, token, dpid):
    uri_get_switch_flow_list = "/restconf/config/opendaylight-inventory:nodes/node/" + dpid + "/"
    response = get_response(ip, port, token, uri_get_switch_flow_list, "GET", "")
    if response == None:
        return None

    json_dict = json.loads(response.read())
    switch_flow_list = json_dict["node"][0]["flow-node-inventory:table"]
    return switch_flow_list

def get_switch_flow_list_in_table(ip, port, token, dpid, table_id):
    uri_get_switch_flow_list_in_table = "/restconf/config/opendaylight-inventory:nodes/node/" + dpid + "/table/" + table_id + "/"
    response = get_response(ip, port, token, uri_get_flow_list_in_table, "GET", "")
    if response == None:
        return None

    json_dict = json.loads(response.read())
    table_flow_list = json_dict["flow-inventory:table"]
    return table_flow_list

def get_switch_flow(ip, port, token, dpid, table_id, flow_id):
    uri_get_switch_flow = "/restconf/config/opendaylight-inventory:nodes/node/" + dpid + "/table/" + table_id + "/flow/" + flow_id + "/"
    response = get_response(ip, port, token, uri_get_flow, "GET", "")
    if response == None:
        return None

    json_dict = json.loads(response.read())
    flow = json_dict["flow-inventory:flow"][0]
    return flow
    
def add_flow_send(ip, port, token, dpid, table_id, flow_id, body):
    uri_flow = "/restconf/config/opendaylight-inventory:nodes/node/" + dpid + "/table/" + table_id + "/flow/" + flow_id + "/"
    # logger.debug(body)
    if table_id == None or flow_id == None:
        print "please input table_id, id"
        return None
    response = get_response(ip, port, token, uri_flow, "PUT", body)
    if response == None:
        return None
    return response

if __name__ == "__main__":
    ip = "192.168.101.220"
    port = "8181"
    username = "admin"
    password = "admin"

    token = login(ip, port, username, password)
    print token
