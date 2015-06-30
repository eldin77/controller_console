import json

def print_all_switches(data, x, file_path):
    from utils import config_json_read
    switches = config_json_read(file_path)
    if data['devices'][x]['role'] == 'MASTER':
        print("-"*47)
        print "| switch name     : %-25s |" %switches[data['devices'][x]['id']] 
        print "| switch dpid     : %-25s |" %data['devices'][x]['id']
        print "| role            : %-25s |" %data['devices'][x]['role']
        print "| mfr             : %-25s |" %data['devices'][x]['mfr']
        print "| switch_type     : %-25s |" %data['devices'][x]['hw']
        print "| switch_version  : %-25s |" %data['devices'][x]['sw']
        print "| protocol        : %-25s |" %data['devices'][x]['annotations']['protocol'] 
        print "| channel id      : %-25s |" %data['devices'][x]['annotations']['channelId'] 
        print("-"*47)

def print_topology(data):
    print("-"*42)
    print "| time       : %-25s |" % data['time']
    print "| devices    : %-25s |" %data['devices']
    print "| links      : %-25s |" %data['links']
    print "| clusters   : %-25s |" %data['clusters']
    print("-"*42)

def print_hosts(data, x):
    print("-"*51)
    print "| id                  : %-25s |" % data['hosts'][x]['id']
    print "| mac                 : %-25s |" %data['hosts'][x]['mac']
    print "| vlan                : %-25s |" %data['hosts'][x]['vlan']
    print "| IP Addresses        : %-25s |" %data['hosts'][x]['ipAddresses']
    print "| Connected device Id : %-25s |" %data['hosts'][x]['location']['elementId']
    print "| Connected port      : %-25s |" %data['hosts'][x]['location']['port'] 
    print("-"*51)



def print_specific_switch(data, file_path):
    from utils import config_json_read
    switches = config_json_read(file_path)
    print("-"*47)
    print "| switch name     : %-25s |" %switches[data['id']]
    print "| switch dpid     : %-25s |" %data['id']
    print "| role            : %-25s |" %data['role']
    print "| mfr             : %-25s |" %data['mfr']
    print "| switch_type     : %-25s |" %data['hw']
    print "| switch_version  : %-25s |" %data['sw']
    print "| protocol        : %-25s |" %data['annotations']['protocol'] 
    print "| channel id      : %-25s |" %data['annotations']['channelId'] 
    print("-"*47)

def print_ports(data, x):
    print("-"*47)
    print "| port            : %-25s |" % data['ports'][x]['port']
    print "| isEnabled       : %-25s |" %data['ports'][x]['isEnabled']
    print "| type            : %-25s |" %data['ports'][x]['type']
    print "| porSpeed        : %-25s |" %data['ports'][x]['portSpeed']
    print "| portName        : %-25s |" %data['ports'][x]['annotations']['portName'] 
    print("-"*47)

def print_specific_switch_flow(data, x):
    print("-"*59)
    print "| id                          : %-25s |" %data['flows'][x]['id']
    print "| appId                       : %-25s |" %data['flows'][x]['appId']
    print "| groupId                     : %-25s |" %data['flows'][x]['groupId']
    print "| priority                    : %-25s |" %data['flows'][x]['priority']
    print "| timeout                     : %-25s |" %data['flows'][x]['timeout']
    print "| isPermanent                 : %-25s |" %data['flows'][x]['isPermanent'] 
    print "| deviceId                    : %-25s |" %data['flows'][x]['deviceId'] 
    print "| state                       : %-25s |" %data['flows'][x]['state']
    print "| life                        : %-25s |" %data['flows'][x]['life']
    print "| packets                     : %-25s |" %data['flows'][x]['packets']
    print "| bytes                       : %-25s |" %data['flows'][x]['bytes'] 
    print "| lastSeen                    : %-25s |" %data['flows'][x]['lastSeen'] 
    instructions_count = len(data['flows'][x]['treatment']['instructions'])
    for n in range(instructions_count):
	        print "| treatment_instroctions_type : %-25s |" %data['flows'][x]['treatment']['instructions'][n]['type']
		print "| treatment_instructions_port : %-25s |" %data['flows'][x]['treatment']['instructions'][n]['port']
    criteria_count = len(data['flows'][x]['selector']['criteria'])
    for m in range(criteria_count):
	        print "| selector_criteria_type      : %-25s |" %data['flows'][x]['selector']['criteria'][m]['type']
		print "| selector_criteria_ethType   : %-25s |" %data['flows'][x]['selector']['criteria'][m]['ethType'] 
       
    print("-"*59)


