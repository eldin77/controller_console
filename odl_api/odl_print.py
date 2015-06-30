MAX_WIDTH = 100
LABELS_PERCENT = 3.0
VALUES_PERCENT = 7.0
MAX_PERCENT = LABELS_PERCENT + VALUES_PERCENT
LABEL_WIDTH = int(MAX_WIDTH * (LABELS_PERCENT / MAX_PERCENT))
VALUE_WIDTH = MAX_WIDTH - LABEL_WIDTH - 3
LINE = "-" * MAX_WIDTH

def print_switch_list(switch_list):
    for switch in switch_list:
        print_switch(switch)

def print_host_list(topology_list):
    for topology in topology_list:
        print LINE
        print_label_and_value("topology-id",topology["topology-id"])
        for node in topology.get("node"):
            node_id = node.get("node-id")
            if node_id.startswith("host:",0,5):
                print_host(node)

def print_topology_list(topology_list):
    for topology in topology_list:
        print_topology(topology)   

def print_switch(switch):
    print LINE
    print_label_and_value("id"          , switch["id"])
    print_label_and_value("ip-address"  , switch["flow-node-inventory:ip-address"])
    print_label_and_value("manufacturer", switch["flow-node-inventory:manufacturer"])
    print_label_and_value("hardware"    , switch["flow-node-inventory:hardware"])
            
def print_host(host):
    print LINE
    print_label_and_value("id"          , host["node-id"])
    print_label_and_value("ip"          , host["host-tracker-service:addresses"][0]["ip"])
    print_label_and_value("mac"         , host["host-tracker-service:addresses"][0]["mac"])
    print_label_and_value("last-seen"   , host["host-tracker-service:addresses"][0]["last-seen"])
    print_label_and_value("first-seen"  , host["host-tracker-service:addresses"][0]["first-seen"])

def print_topology(topology):
    print LINE
    print_label_and_value("topology-id" , topology["topology-id"])
    for link in topology.get("link"):
        print LINE
        print_label_and_value("link-id" , link["link-id"])
        print LINE
        print_label_and_value("src-node", link["source"]["source-node"])
        print_label_and_value("src-tp"  , link["source"]["source-tp"])
        print_label_and_value("dst-node", link["destination"]["dest-node"])
        print_label_and_value("dst-tp"  , link["destination"]["dest-tp"])

def print_switch_port(switch_port):
    print LINE
    print_label_and_value("id", switch_port["id"])
    print_label_and_value("name", switch_port["flow-node-inventory:name"])
    print_label_and_value("mac", switch_port["flow-node-inventory:hardware-address"])
    print_label_and_value("port-number", switch_port["flow-node-inventory:port-number"])
    # port statistics info
    port_statistics = switch_port.get("opendaylight-port-statistics:flow-capable-node-connector-statistics")
    print_label_and_value("receive-drop", port_statistics.get("receive-drops"))
    print_label_and_value("transmit-drop", port_statistics.get("transmit-drops"))
    # port byte statistics info
    port_byte = port_statistics.get("bytes")
    print_label_and_value("byte-received", port_byte.get("received"))
    print_label_and_value("byte-transmitted", port_byte.get("transmitted"))
    # port packet sttistics info
    port_packet = port_statistics.get("packets")
    print_label_and_value("packet-received", port_packet.get("received"))
    print_label_and_value("packet-transmitted", port_packet.get("transmitted"))

def print_switch_port_list(port_list):
    for port in port_list:
        print_switch_port(port)

def print_switch_flow(flow):
    print LINE
    print_label_and_value("id", flow.get("id"))
    print_label_and_value("flow_name", flow.get("flow-name"))
    print_label_and_value("table_id", flow.get("table_id"))
    print_label_and_value("priority", flow.get("priority"))
    print_label_and_value("tos", flow.get("tos"))
    # match info
    match = flow.get("match")
    if match:
        # ipv4 info
        print_label_and_value("ipv4_dst",match.get("ipv4-destination"))
        print_label_and_value("ipv4_src",match.get("ipv4-source"))

        # port-number info
        print_label_and_value("dst_port", match.get("udp_destination_port"))
        print_label_and_value("src_port", match.get("udp_source_port"))

        # ethernet match info
        eth_match = match.get("ethernet-match")
        if eth_match:
            eth_dst = eth_match.get("ethernet-destination")
            if eth_dst:
                print_label_and_value("eth_dst", eth_dst("address"))
                print_label_and_value("eth_dst_mask", eth_dst.get("mask"))
            eth_src = eth_match.get("ethernet-source")
            if eth_src:
                print_label_and_value("eth_src", eth_src("address"))
                print_label_and_value("eth_src_mask", eth_src.get("mask"))
            eth_type = eth_match.get("ethernet-type")
            if eth_type:
                print_label_and_value("eth_type", eth_type.get("type"))
        # ip match info
        ip_match = flow.get("ip-match")
        if ip_match:
            print_label_and_value("ip-protocol", ip_match.get("ip-protocol"))
        
        # vlan match info
        vlan_match = flow.get("vlan-match")
        if vlan_match:
            print_label_and_value("vlan-id", vlan_match.get("vlan-id"))

        # apply instruction info
        instructions = flow.get("instructions")
        if instructions:
            instruction_list = instructions.get("instruction")
            if instruction_list:
                for instruction in instruction_list:
                    print_label_and_value("order", instruction.get("order"))
                    # actions info
                    apply_action = instruction.get("apply-actions")
                    if apply_action:
                        action_list = apply_action.get("action")
                        if action_list:
                            for action in action_list:
                                print_label_and_value("action_order", action.get("order"))
                                output_action = action.get("output-action")
                                if output_action:
                                    print_label_and_value("output_action", output_action.get("output-node-connector"))

def print_switch_flow_list_in_table(table):
    print LINE
    print_label_and_value("table_id",table.get("id"))
    flow_list = table.get("flow")
    if flow_list:
        for flow in flow_list:
            print_switch_flow(flow)

def print_switch_flow_list(table_list):
    print "table lenght = " , len(table_list)
    for table in table_list:
        print_switch_flow_list_in_table(table)

def matrix_print(print_dict):
    labels_size = int(MAX_WIDTH * (LABELS_PERCENT / (MAX_PERCENT)))
    values_size = MAX_WIDTH - labels_size - 3
    print "-" * MAX_WIDTH
    for key, value in print_dict.iteritems():
        print_label_and_value(key, value)

def print_label_and_value(label, value):
    '''
    value_size = len(value)
    multi = int() # value size over MAX_WIDTH size
    multi = int(MAX_WIDTH / value_size) + 1
    '''
    print "|" + label.ljust(LABEL_WIDTH) + "|" + str(value).ljust(VALUE_WIDTH) + "|"

    
if __name__ == "__main__":
    print "test"

    test_dic = {
        "test" : 1,
        "test2": 2,
        "test3": 3
    }
    matrix_print(test_dic.keys(), test_dic.values())
