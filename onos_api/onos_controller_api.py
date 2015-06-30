import httplib
import json
import urllib2
import traceback

def send_rest_api_request(headers, conn, url, body, method):
    try:
        conn.request(method, url, body, headers)
    except Exception:
        print "Ports request Error"
        traceback.print_exc()
        return None
 
    response = conn.getresponse()
    if response.status in [httplib.OK]:
        response = json.loads(response.read())
    else:
        print "Error: failed, http response status: %s" % response.status
        conn.close()
    return response

def onos_api_login(ip, port, user, password):
    body = {"login": {"user":user,"password":password,"domain":"sdn"}} 
    headers = {"Content-Type":"application/json"}
    url = "https://"+str(ip)+":"+str(port)+"/onos/v1/auth"
    try :
        conn = httplib.HTTPConnection(str(ip), int(port))
    except Exception:
        traceback.print_exc()
        return None 
    token = send_rest_api_request(headers, conn, url, json.dumps(body), "POST")
    return token

def onos_api_switches(ip, port, token):
    headers = {"X-Auth-Token":token}
    conn = httplib.HTTPConnection(str(ip), int(port))
    url = 'http://'+ip+':'+port+'/onos/v1/devices'
    response = send_rest_api_request(headers, conn, url, None, "GET")
    return response

def onos_api_topology(ip, port, token):
    headers = {"X-Auth-Token":token}
    conn = httplib.HTTPConnection(str(ip), int(port))
    url = 'http://'+ip+':'+port+'/onos/v1/topology'
    response = send_rest_api_request(headers, conn, url, None, "GET")
    return response

def onos_api_hosts(ip, port, token):
    headers = {"X-Auth-Token":token}
    conn = httplib.HTTPConnection(str(ip), int(port))
    url = 'http://'+ip+':'+port+'/onos/v1/hosts'
    response = send_rest_api_request(headers, conn, url, None, "GET")
    return response

def onos_api_specific_switch(ip, port, switch_dpid, token):
    headers = {"X-Auth-Token":token}
    conn = httplib.HTTPConnection(str(ip), int(port))
    url = 'http://'+ip+':'+port+'/onos/v1/devices/'+switch_dpid
    response = send_rest_api_request(headers, conn, url, None, "GET")
    return response

def onos_api_ports(ip, port, switch_dpid, token):
    headers = {"X-Auth-Token":token}
    conn = httplib.HTTPConnection(str(ip), int(port))
    url = 'http://'+ip+':'+port+'/onos/v1/devices/'+switch_dpid+'/ports'
    response = send_rest_api_request(headers, conn, url, None, "GET")
    return response

def onos_api_flows(ip, port, switch_dpid, token):
    headers = {"X-Auth-Token":token}
    conn = httplib.HTTPConnection(str(ip), int(port))
    url = 'http://'+ip+':'+port+'/onos/v1/flows/'+switch_dpid
    response = send_rest_api_request(headers, conn, url, None, "GET")
    return response

def onos_api_add_datapath_flows(ip, port, token, switch_dpid, body, print_flag):
    headers = {"X-Auth-Token":token}
    conn = httplib.HTTPSConnection(str(ip), int(port))
    url = "https://"+str(ip)+":"+str(port)+"/sdn/v1.1.0/of/datapaths/"+switch_dpid+"/flows"
    print body, url
    response = send_rest_api_request(headers, conn, url, body, "POST")
    return response

def onos_api_delete_datapath_flows(ip, port, token, switch_dpid, body, print_flag):
    headers = {"X-Auth-Token":token}
    conn = httplib.HTTPSConnection(str(ip), int(port))
    url = "https://"+str(ip)+":"+str(port)+"/onos/v1/datapaths/"+switch_dpid+"/flows"
    print body, url
    response = send_rest_api_request(headers, conn, url, body, "DELETE")
    return response

def onos_api_update_datapath_flows(ip, port, token, switch_dpid, body, print_flag):
    headers = {"X-Auth-Token":token}
    conn = httplib.HTTPSConnection(str(ip), int(port))
    url = "https://"+str(ip)+":"+str(port)+"/onos/v1/datapaths/"+switch_dpid+"/flows"
    print body, url
    response = send_rest_api_request(headers, conn, url, body, "PUT") 
    return response





