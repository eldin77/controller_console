import json
import traceback
import os

def create_controller_db(file_path, ip, port, token):
    from utils import config_json_write
    from onos_api.onos_controller_api import onos_api_switches
    
    switches = {}
    switch_data = onos_api_switches(ip, port, token)['devices'] 
    for switch in switch_data:
        if switch['role'] == 'MASTER':
            switches[switch['id']] = switch['id']

    config_json_write(file_path, switches)

def update_controller_db(file_path, ip, port, token):
    from utils import config_json_read, config_json_write   
    from onos_api.onos_controller_api import onos_api_switches
    
    latest_switches = {}
    latest_sw_data = onos_api_switches(ip, port, token)['devices']
    switches = config_json_read(file_path)
    for  switch in latest_sw_data:
        if switch['role'] == 'MASTER':
            try:
                sw_alias = switches[switch['id']]
            except KeyError:
                sw_alias = switch['id']
            finally:
                latest_switches[switch['id']] = sw_alias
                         
    config_json_write(file_path, latest_switches)
    


def refresh_con_db(file_path, ip, port, token):
    import os
    if not os.path.exists(file_path):
        create_controller_db(file_path, ip, port, token)
    else:
        update_controller_db(file_path, ip, port, token)

def return_sw_names(file_path):
    from utils import config_json_read
    
    switches = config_json_read(file_path)
    return switches.values()

def return_sw_dpid(file_path, switch_alias):
    from utils import config_json_read
    
    sw_dpid = str()
    switches = config_json_read(file_path)
    for dpid in switches.keys():
        if switches[dpid] == switch_alias:
            sw_dpid = dpid
            break
    return sw_dpid  

