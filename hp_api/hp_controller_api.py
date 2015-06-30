import httplib
import urllib
import json
import hashlib
import os
import commands
import urlparse
import traceback 
from registered_controller import *
from array import *
from errno import *
from hp_api.hp_result_print import *
from global_value import *
from utils import *

#tmp
username = "sdn"
password = "skyline"
controller_ip = "192.168.101.76"
#controller_ip = "10.10.0.160"
controller_port = 8443
controller_type = "HP" 
controller_name = "HP Controller" 
dpids = []

def send_rest_api_request(headers, conn, url, body, method):
    try:
        conn.request(method, url, body, headers)
    except Exception:
        print "Ports requeest Error"
        traceback.print_exc()
        return None

    response = conn.getresponse()
    if response.status in [httplib.OK]:
        response = json.loads(response.read())
    else:
        print "error: port stats failed, http response status: %s" % response.status
        conn.close()
    return response


def hp_api_license(ip, port, token):
    headers = {"X-Auth-Token":token}
    conn = httplib.HTTPSConnection(str(ip), int(port))
    url = "https://"+str(ip)+":"+str(port)+"/sdn/v2.0/licenses"

    try:
        conn.request("GET", url, None, headers)
    except:
        print "license requeest Error"
        return None

    response = conn.getresponse()
    if response.status in [httplib.OK]:
        response = json.loads(response.read())
    else:
        print "error: login failed, http response status: %s" % response.status
        conn.close()
    try:
        print_license(response['record'])
    except KeyError as msg:
        print "license Not Registered",msg
    return response

def hp_api_version(ip, port, token, print_flag):
    headers = {"Content-Type":"application/json"}
    url = "https://"+str(ip)+":"+str(port)+"/sdn/v2.0"
    try :
        conn = httplib.HTTPSConnection(str(ip), int(port))
    except Exception:
        traceback.print_exc()
        return None 

    response = send_rest_api_request(headers, conn, url, None, "GET")

    if print_flag:
        try:
            print_controller_version(response['version'])
        except Exception:
            print "HP Controller version error"
            traceback.print_exc()
            return None 

    return response

def hp_api_login(ip, port, user, password):
    body = {"login": {"user":user,"password":password,"domain":"sdn"}} 
    headers = {"Content-Type":"application/json"}
    url = "https://"+str(ip)+":"+str(port)+"/sdn/v2.0/auth"
    try :
        conn = httplib.HTTPSConnection(str(ip), int(port))
    except Exception:
        traceback.print_exc()
        return None 

    response = send_rest_api_request(headers, conn, url, json.dumps(body), "POST")

    try:
        print_login_token(response['record'])
    except Exception:
        print "HP Controller login error"
        traceback.print_exc()
        return None 

    return response['record']

def read_conf(file_path):
    controllers = []
    try:
        f = open(file_path)
    except IOError as msg:
        print msg
        return None

    line = f.readline()
    while line:
        json_line = json.loads(line)
        line = f.readline()
        #controllers.append(split_line[0]+":"+split_line[2])
    return json_line 

def read_json_conf(file_path):
    controllers = []
    with open(file_path,"r") as read_file:
        json_data = json.load(read_file)
        read_file.close()
    return json_data

def hp_api_stats(ip, port, token, print_flag):
    headers = {"X-Auth-Token":token}
    conn = httplib.HTTPSConnection(str(ip), int(port))
    url = "https://"+str(ip)+":"+str(port)+"/sdn/v2.0/of/stats"

    try:
        conn.request("GET", url, None, headers)
    except:
        print "license requeest Error"
        return None

    response = conn.getresponse()
    if response.status in [httplib.OK]:
        response = json.loads(response.read())
    else:
        print "error: login failed, http response status: %s" % response.status
        conn.close()

    if print_flag:
        try:
            print_switch_stats(response['controller_stats'][0])
        except Exception:
            traceback.print_exc()
            print "Switch Not Registered"

    return response

def hp_api_ports(ip, port, token, print_flag):
    headers = {"X-Auth-Token":token}
    conn = httplib.HTTPSConnection(str(ip), int(port))
    url = "https://"+str(ip)+":"+str(port)+"/sdn/v2.0/of/stats/ports"

    response = send_rest_api_request(headers, conn, url, None, "GET")

    if print_flag :
        try:
            datapath_count = len(response['stats'])
            for x in range(datapath_count):
                print_ports(response['stats'][x])
        except Exception:
            traceback.print_exc()

    return response

def hp_api_get_datapaths(ip, port, token):
    headers = {"X-Auth-Token":token}
    conn = httplib.HTTPSConnection(str(ip), int(port))
    url = "https://"+str(ip)+":"+str(port)+"/sdn/v2.0/of/datapaths"
    response = send_rest_api_request(headers, conn, url, None, "GET")
#    datapath_count = len(response['datapaths'])

#    for x in range(datapath_count):
#        print_datapaths(response['datapaths'][x], dpids)

    return response

def hp_api_get_datapath(ip, port, token, dpid, sw_name, print_flag):
    headers = {"X-Auth-Token":token}
    conn = httplib.HTTPSConnection(str(ip), int(port))
    url = "https://"+str(ip)+":"+str(port)+"/sdn/v2.0/of/datapaths/"+dpid

    response = send_rest_api_request(headers, conn, url, None, "GET")
    if print_flag:
        print_datapath(response['datapath'], sw_name)
    return response

def hp_api_get_datapath_port(ip, port, token, dpid, print_flag):
    headers = {"X-Auth-Token":token}
    conn = httplib.HTTPSConnection(str(ip), int(port))
    url = "https://"+str(ip)+":"+str(port)+"/sdn/v2.0/of/datapaths/"+str(dpid.strip('"'))+"/ports"

    response = send_rest_api_request(headers, conn, url, None, "GET")

    if response != None:
        port_count = len(response['ports'])
        version = response['version']
        if print_flag:
            for x in range(port_count):
                print_datapath_ports(response['ports'][x], dpid, version)
            #print dpid, response['ports'][x]['mac']

    return response

def hp_api_get_datapath_flows(ip, port, token, dpid, print_flag):
    headers = {"X-Auth-Token":token}
    conn = httplib.HTTPSConnection(str(ip), int(port))
    url = "https://"+str(ip)+":"+str(port)+"/sdn/v2.0/of/datapaths/"+str(dpid.strip('"'))+"/flows"

    response = send_rest_api_request(headers, conn, url, None, "GET")

    if response != None:
        try:
            flows_count = len(response['flows'])
            version = response['version']
            if print_flag:
                for x in range(flows_count):
                    print_datapath_flows(response['flows'][x], dpid, version)
        except Exception:
            print "No Flows"
            #traceback.print_exc()
    return response

def hp_api_add_datapath_flows(ip, port, token, dpid, body, print_flag):
    headers = {"X-Auth-Token":token}
    conn = httplib.HTTPSConnection(str(ip), int(port))
    url = "https://"+str(ip)+":"+str(port)+"/sdn/v2.0/of/datapaths/"+dpid+"/flows"
    print body, url
    response = send_rest_api_request(headers, conn, url, body, "POST")

    """
    if response != None:
        try:
            flows_count = len(response['flows'])
            version = response['version']
            if print_flag:
                for x in range(flows_count):
                    print_datapath_flows(response['flows'][x], dpid, version)
        except Exception:
            print "No Flows"
            #traceback.print_exc()
    """
    return response


def get_controller_conf(file_path):
    #controllers = read_conf(file_path)
    json_data = read_json_conf(file_path)
    return json_data

def show_openflow_switch_info(ip, port, token ,sw_name, dpid, print_flag):
    hp_api_get_datapath(ip, port, token, dpid, sw_name, print_flag)
    hp_api_get_datapath_flows(ip, port, token, dpid, print_flag)
    hp_api_get_datapath_port(ip, port, token, dpid, print_flag)

def main():
    token = hp_api_login(controller_ip, controller_port, "sdn", "skyline")
    #test = get_controller_conf()
    #response = hp_api_stats(controller_ip, controller_port, token['token'], 1)
    #response = hp_api_ports(controller_ip, controller_port, token['token'], 1)
    #response = hp_api_get_datapaths(token['token'])
    #dpid_count = len(dpids)
    response = hp_api_version(controller_ip, controller_port, token, 1)
    body ={"flow": {"actions": [{"output": 1}], "priority": 2999, "match": [{"ipv4_dst": "192.168.200.12"}, {"ipv4_src": "192.168.200.11"}, {"eth_type": "ipv4"}]}}
    dpid = "00:00:00:00:00:00:00:01"
    response = hp_api_add_datapath_flows(controller_ip, controller_port, token['token'],dpid, json.dumps(body), 1)
    print response

    #for x in range(dpid_count):
    #    hp_api_get_datapath_port(controller_ip, controller_port, token['token'], dpids[x], 1)
    #    hp_api_get_datapath_flows(controller_ip, controller_port,token['token'], dpids[x],1)

if __name__ == "__main__":
    main()
