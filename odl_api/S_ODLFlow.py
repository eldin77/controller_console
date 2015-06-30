import cmd
import json
import global_value
import utils
import odl_api
import logging

debug = True
LOG_PATH = "test.log"
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(filename=LOG_PATH, format=FORMAT)
logger = logging.getLogger('root')
if debug:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

PROMPT = "Flow(<dpid>) # "
class S_ODLFlow(cmd.Cmd):
    MATCH_REGEX = {
        "id" : '',
        "flow_name" : '',
        "table_id" : '',
        "priority" : '',
        "tos" : '',
        "ipv4_dst" : '',
        "ipv4_src" : '',
        "tcp_dst_port" : '',
        "tcp_src_port" : '',
        "udp_dst_port" : '',
        "udp_src_port" : '',
        "eth_dst" : '',
        "eth_dst_mask" : '',
        "eth_src" : '',
        "eth_src_mask" : '',
        "eth_type" : '',
        "ip_protocol" : '',
        "vlan_id" : '',
        "in_port" : '',
        "apply":'',
    }

    def do_quit(self, cmd_input):
        return True

    def do_exit(self, cmd_input):
        return True

    def do_EOF(self, cmd_input):
        return True

    def F_Start(self, ip, port, token, dpid, flow_id):
        self.ip = ip
        self.port = port
        self.token = token
        self.dpid = dpid
        self.input_match = {
            "id" : flow_id,
            "table_id" : "0"
        }
        self.prompt = "Flow(" + flow_id + ") # "
        self.json_body = None
        self.cmdloop()

    def do_match(self, cmd_input):
        args = cmd_input.split()
        if len(args) < 2:
            print "please input <MATCH_KEY> <argument> ..."
            return None
        match_key = args[0]
        values = args[1:]
        if not self.MATCH_REGEX.has_key(match_key):
            print "invalid input match key"
            return None
        
        if match_key == "apply":
            if not len(values) == 3:
                print "apply need 3 arguments"
                return False

            self.set_apply(args[1:])
            return None
        else :
            if not len(values) == 1:
                print match_key + " need 1 arguments "
                return None
            #TODO value validation check
            self.input_match[match_key] = values[0]

    def set_apply(self, args):
        flag = True
        while(flag):
            instruction_order = args[0]
            if not self.input_order_check(instruction_order):
                continue
            action_order = args[1]
            if not self.input_order_check(action_order):
                continue
            
            output_action = args[2]
            if len(output_action.split()) == 0:
                print "please input output action"
                continue
            flag = False
         

        match_apply = self.input_match.get("apply")
        if match_apply == None:
            self.input_match["apply"] = {
                instruction_order : {
                    action_order : output_action
                }
            }
        elif match_apply.get(instruction_order) :
            match_apply[instruction_order][action_order] = output_action
        else :
            match_apply[instruction_order] = { action_order : output_action }
    
    def input_order_check(self, order):
        try:
            int(order)
        except ValueError:
            print "please input Number"
            return False
        else:
            return True

    def do_apply(self, cmd_input):
        json_body = "{\
            \"flow-node-inventory:flow\":{\
                <match>,\
                \"instructions\" : <apply>\
            }\
        }"
        match = self.match_parse()
        match_apply = self.apply_parse()

        json_body = json_body.replace("<match>",match)
        json_body = json_body.replace("<apply>",match_apply)
        flow_dict = json.loads(json_body)
        self.json_body = json.dumps(flow_dict).replace("\"None\"","null")
        print self.json_body

    def match_parse(self):
        match_body = "\
                    \"id\": \"<id>\",\
                    \"table_id\": \"<table_id>\",\
                    \"priority\": \"<priority>\",\
                    \"tos\": \"<tos>\",\
                    \"match\": {\
                        \"in-port\": \"<in_port>\",\
                        \"ipv4-destination\": \"<ipv4_dst>\",\
                        \"ipv4-source\": \"<ipv4_src>\",\
                        \"tcp-destination-port\": \"<tcp_dst_port>\",\
                        \"tcp-source-port\": \"<tcp_src_port>\",\
                        \"udp-destination-port\": \"<udp_dst_port>\",\
                        \"udp-source-port\": \"<udp_src_port>\",\
                        \"ip-match\": {\
                                \"ip-protocol\": \"<ip_protocol>\"\
                        },\
                        \"vlan-match\": {\
                            \"vlan-id\": \"<vlan_id>\"\
                        },\
                        \"ethernet-match\": {\
                            \"ethernet-destination\":{\
                                \"address\":\"<eth_dst>\",\
                                \"mask\":\"<eth_dst_mask>\"\
                            },\
                            \"ethernet-source\": {\
                                \"address\":\"<eth_src>\",\
                                \"mask\":\"<eth_src_mask>\"\
                            },\
                            \"ethernet-type\": {\
                                \"type\": \"<eth_type>\"\
                            }\
                        }\
                    }\
        "
        for match_key in self.MATCH_REGEX:
            value = str(self.input_match.get(match_key))
            if value :
                match_body = match_body.replace("<" + match_key + ">", value)
            else :
                match_body = match_body.replace("\"<" + match_key +">\"" , "null")
        return match_body

    def apply_parse(self):
        instructions = {
            "instruction":[]
        }
        instruction_order_list = self.input_match.get("apply")
        if instruction_order_list == None:
            return "null"
        for instruction_order, action_order_list in instruction_order_list.iteritems():
            instruction = {
                "order" : instruction_order,
                "apply-actions" : {
                    "action" : []
                }
            }
            for action_order,output_action in action_order_list.iteritems():
                action = {
                    "order" : action_order,
                    "output-action" : {
                        "output-node-connector" : output_action
                    }
                }
                instruction["apply-actions"]["action"].append(action)
            instructions["instruction"].append(instruction)

        return json.dumps(instructions)

    def do_save(self, cmd_input):
        if self.json_body == None:
            print "please apply match"
        else :
            file_path = global_value.FLOW_PATH + "/" + self.input_match["table_id"] + "-" + self.input_match["id"] + ".json"
            utils.config_json_write(file_path, self.json_body)
            print "save : " + file_path

    def do_send(self, cmd_input):
        table_id = self.input_match.get("table_id")
        flow_id = self.input_match.get("id")
        if table_id == None or flow_id == None:
            print "please input table_id, flow_id"
            return None
        
        if self.json_body == None:
            print "please apply match"
            return None
        response = odl_api.add_flow_send(self.ip, self.port, self.token, self.dpid, table_id, flow_id, self.json_body)
        if response:
            print "send flow"

    def complete_match(self, text, line, begidx, endidx):
        if not text:
            completions = self.MATCH_REGEX.keys()
        else:
            completions = [match for match in self.MATCH_REGEX.keys()
                            if match.startswith(text)
                        ]
        return completions

        

if __name__ == "__main__":
    ip = "10.0.2.102"
    port = "8181"
    token = odl_api.login(ip, port, "admin", "admin")
    test_console = S_ODLFlow()
    test_console.debug = True
    test_console.F_Start(ip, port, token, "openflow:515", "testtest")
