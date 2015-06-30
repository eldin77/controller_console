import json

def print_login_token(record):
	print("-"*68)
	print "| token			: %-40s |"% json.dumps(record['token'])
	print "| expiration		: %-40s |"% json.dumps(record['expiration'])
	print "| expirationData	: %-40s |"% json.dumps(record['expirationDate'])
	print "| userId		: %-40s |"% json.dumps(record['userId'])
	print "| userName		: %-40s |"% json.dumps(record['userName'])
	print "| domainId		: %-40s |"% json.dumps(record['domainId'])
	print "| domainName		: %-40s |"% json.dumps(record['domainName'])
	print("-"*68)

def print_license(record):
	print("-"*68)
	print "| install_id		: %-40s |"% json.dumps(record['instaal_id'])
	print "| serial_no		: %-40s |"% json.dumps(record['serail_no'])
	print "| license_metric		: %-40s |"% json.dumps(record['license_metric'])
	print "| product		: %-40s |"% json.dumps(record['product'])
	print "| metric_qty		: %-40s |"% json.dumps(record['metric_qty'])
	print "| license_type		: %-40s |"% json.dumps(record['license_type'])
	print "| base_license		: %-40s |"% json.dumps(record['base_license'])
	print "| creation_date		: %-40s |"% json.dumps(record['creation_date'])
	print "| activated_date		: %-40s |"% json.dumps(record['activated_date'])
	print "| expiry_date		: %-40s |"% json.dumps(record['expiry_date'])
	print "| license_status		: %-40s |"% json.dumps(record['license_status'])
	print "| deactivated_key	: %-40s |"% json.dumps(record['deactivated_key'])
	print("-"*68)

def print_controller_list(controllers):
	print("-"*68)
	print "| Controller type	: %-40s |"% json.dumps(controllers['type'])
	print "| Alise			: %-40s |"% json.dumps(controllers['name']) 
	print "| Controller ip		: %-40s |"% json.dumps(controllers['ip'])
	print "| Controller port	: %-40s |"% json.dumps(controllers['port'])
	print "| Connected Switch	: %-40s |"% "UNKNOWN" 
	print "| Status 		: %-40s |"% "UNKNOWN" 
	print("-"*68)

def print_switch_stats(response):
	print("-"*68)
	print "| Msg In		: %-40s |"% json.dumps(response['msg_in'])
	print "| UID			: %-40s |"% json.dumps(response['uid'])
	print "| Lost Bytes		: %-40s |"% json.dumps(response['lost']['bytes'])
	print "| Lost Packets		: %-40s |"% json.dumps(response['lost']['packets'])
	print "| Packet Out Bytes 	: %-40s |"% json.dumps(response['packet_out']['bytes'])
	print "| Packet Out Packets	: %-40s |"% json.dumps(response['packet_out']['packets'])
	print "| Packet In Bytes	: %-40s |"% json.dumps(response['packet_in']['bytes'])
	print "| Packet In Packets 	: %-40s |"% json.dumps(response['packet_in']['packets'])
	print "| Duration ms 		: %-40s |"% json.dumps(response['duration_ms'])
	print "| Msg Out 		: %-40s |"% json.dumps(response['msg_out'])
	print("-"*68)

def print_port_stats(response):
	print "| Port ID		: %-40s |"% json.dumps(response['port_id'])
	print("-"*68)
	print "| Collisions		: %-40s |"% json.dumps(response['collisions'])
	print "| Duration nsec		: %-40s |"% json.dumps(response['duration_nsec'])
	print "| Duration sec		: %-40s |"% json.dumps(response['duration_sec'])
	print "| Rx Bytes 		: %-40s |"% json.dumps(response['rx_bytes'])
	print "| Rx Crc Err 		: %-40s |"% json.dumps(response['rx_crc_err'])
	print "| Rx Dropped		: %-40s |"% json.dumps(response['rx_dropped'])
	print "| Rx Errors		: %-40s |"% json.dumps(response['rx_errors'])
	print "| Rx Frame Err 		: %-40s |"% json.dumps(response['rx_frame_err'])
	print "| Rx Over Err 		: %-40s |"% json.dumps(response['rx_over_err'])
	print "| Rx Packets		: %-40s |"% json.dumps(response['rx_packets'])
	print "| Tx Bytes		: %-40s |"% json.dumps(response['tx_bytes'])
	print "| Tx Dropped		: %-40s |"% json.dumps(response['tx_dropped'])
	print "| Tx Errors		: %-40s |"% json.dumps(response['tx_errors'])
	print "| Tx Packets		: %-40s |"% json.dumps(response['tx_packets'])
	print("-"*68)

def print_ports(response):
	port_count = len(response['port_stats']) 
	print("-"*68)
	print "| DPID			: %-40s |"% json.dumps(response['dpid'])
	print("="*68)
	for x in range(port_count):
		print_port_stats(response['port_stats'][x])
	print "| Version	 	: %-40s |"% json.dumps(response['version'])
	print("-"*68)

def print_datapaths(response, switch_alias):
	dpid = []
	capabilities_count =  len(response['capabilities'])
	dpid.append(json.dumps(response['dpid']))
	print("-"*68)
	print "| Switch Alias		: %-40s |"% switch_alias 
	print "| DPID	 		: %-40s |"% json.dumps(response['dpid'])
	print "| Device IP		: %-40s |"% json.dumps(response['device_ip'])
	print "| Last Message	 	: %-40s |"% json.dumps(response['last_message'])
	print "| Num Buffers	 	: %-40s |"% json.dumps(response['num_buffers'])
	for x in range(capabilities_count):
		print "| Capabilities	 	: %-40s |"% json.dumps(response['capabilities'][x])
	print "| Device Port	 	: %-40s |"% json.dumps(response['device_port'])
	print "| Ready	 		: %-40s |"% json.dumps(response['ready'])
	print "| Num Tables	 	: %-40s |"% json.dumps(response['num_tables'])
	print "| Negotiated Version	: %-40s |"% json.dumps(response['negotiated_version'])
	print("-"*68)

def print_datapath(response, switch_alias):
	capabilities_count =  len(response['capabilities'])
	print("-"*68)
	print "| Switch Alias		: %-40s |"% switch_alias 
	print "| DPID	 		: %-40s |"% json.dumps(response['dpid'])
	print "| Device IP		: %-40s |"% json.dumps(response['device_ip'])
	print "| Last Message	 	: %-40s |"% json.dumps(response['last_message'])
	print "| Num Buffers	 	: %-40s |"% json.dumps(response['num_buffers'])
	for x in range(capabilities_count):
		print "| Capabilities	 	: %-40s |"% json.dumps(response['capabilities'][x])
	print "| Device Port	 	: %-40s |"% json.dumps(response['device_port'])
	print "| Ready	 		: %-40s |"% json.dumps(response['ready'])
	print "| Num Tables	 	: %-40s |"% json.dumps(response['num_tables'])
	print "| Negotiated Version	: %-40s |"% json.dumps(response['negotiated_version'])
	print("-"*68)

def print_datapath_ports(response, dpid, version):
	print("-"*68)
	print "| DPID	 		: %-40s |"% dpid
	print "| Version	 	: %-40s |"% version 
	print "| Advertised Features	: %-40s |"% json.dumps(response['advertised_features'])
	print "| Config		: %-40s |"% json.dumps(response['config'])
	print "| Current Features	: %-40s |"% json.dumps(response['current_features'])
	#print "| Current Speed		: %-40s |"% json.dumps(response['current_speed'])
	print "| ID			: %-40s |"% json.dumps(response['id'])
	print "| MAC			: %-40s |"% json.dumps(response['mac'])
	#print "| MAX Speed		: %-40s |"% json.dumps(response['max_speed'])
	print "| Name			: %-40s |"% json.dumps(response['name'])
	print "| Peer Features		: %-40s |"% json.dumps(response['peer_features'])
	print "| State			: %-40s |"% json.dumps(response['state'])
	#print "| Supported Features		: %-40s |"% json.dumps(response['advertised_features'])
	print("-"*68)

def print_datapath_flows(response, dpid, version):
	print("-"*68)
	print "| DPID		 	: %-40s |"% dpid 
	print "| packet_count	 	: %-40s |"% json.dumps(response['packet_count'])
	print "| hard_timeout	 	: %-40s |"% json.dumps(response['hard_timeout'])
	print "| byte_count		: %-40s |"% json.dumps(response['byte_count'])
	print "| idle_timeout		: %-40s |"% json.dumps(response['idle_timeout'])
	print "| actions		: %-40s |"% json.dumps(response['actions'])
	print "| duration_nsec		: %-40s |"% json.dumps(response['duration_nsec'])
	print "| priority		: %-40s |"% json.dumps(response['priority'])
	print "| duration_sec		: %-40s |"% json.dumps(response['duration_sec'])
	print "| cookie		: %-40s |"% json.dumps(response['cookie'])
	print "|","-"*25,"Match Fields","-"*25,"|"
	match = response['match']
	match_fields = len(match)
	for x in range(match_fields):
		key = json.dumps(match[x].keys()).split('"')
		print "| %s		" % key[1],": %-40s |" % response['match'][x][key[1]]
		#print key[1] ,":", response['match'][x][key[1]]
	print("-"*68)

def print_controller_version(response):
	print("-"*68)
	print "| Controller Version	: %-40s |"% json.dumps(response['build'])
	print "| Status		: %-40s |"% json.dumps(response['status'])
	print("-"*68)

