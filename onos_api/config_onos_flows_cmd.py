import cmd
import traceback
import os
from onos_api.onos_utils import *
from onos_api.onos_controller_api import *

class S_ONOSFlows(cmd.Cmd):
    from global_value import FLOW_PATH
    instruction_command = ['drop', 'forward']
    match_second_command = ['in_port',
                            'eth_src',
                            'eth_dst',
                            'ipv4_src',
                            'ipv4_dst',
                            'eth_type',
                            'protocol',
                            'srcport',
                            'dstport',
                            'vlanid',
                            'vlanpriority',
                            'tos',
                            'apply']

    def __init__(self, completekey = 'tab', stdin=None, stdout=None):

        import sys
        if stdin is not None:
            self.stdin = stdin
        else:
            self.stdin = sys.stdin
        if stdout is not None:
            self.stdout = stdout
        else:
            self.stdout = sys.stdout

        self.cmdqueue = []
        self.completekey = completekey
        self.match_set_func = {}
        self.list_match_field = []
        self.priority = 10000 
        self.idle_timeout = 60 
        self.instruction = []
        self.make_json_flow = {}
        self.match_funcs = [self.onos_flow_set_inport,
                        self.onos_flow_set_src_mac,
                        self.onos_flow_set_dst_mac,
                        self.onos_flow_set_src_ip,
                        self.onos_flow_set_dst_ip,
                        self.onos_flow_set_ethertype,
                        self.onos_flow_set_protocol,
                        self.onos_flow_set_src_port,
                        self.onos_flow_set_dst_port,
                        self.onos_flow_set_vlan_id,
                        self.onos_flow_set_vlan_priority,
                        self.onos_flow_set_tos,
                        self.onos_flow_set_match_apply]
        self.match_check_func = []

        for x in range(len(self.match_second_command)):
            try:
                self.match_set_func[self.match_second_command[x]] = self.match_funcs[x]
            except Exception:
                traceback.print_exc()

    def __call__(self, *args):
        self.ip = args[0]
        self.port = args[1]
        self.token = args[2]
        self.dpid = args[3]
        self.flow_name = args[4]
        return None

    def onos_flow_set_inport(self, in_port):
        m_in_port = {"inport": in_port}
        self.list_match_field.append(m_in_port)

    def onos_flow_set_src_mac(self, eth_src):
        from utils import checkmac
        checkmac(eth_src)
        m_eth_src = {"eth_src":eth_src}
        self.list_match_field.append(m_eth_src)

    def onos_flow_set_dst_mac(self, eth_dst):
        from utils import checkmac
        checkmac(eth_dst)
        m_eth_dst = {"eth_dst":eth_dst}
        self.list_match_field.append(m_eth_dst)

    def onos_flow_set_src_ip(self, src_ip):
        from utils import ip_check
        if ip_check(src_ip) != None:
            m_src_ip = {"ipv4_src":src_ip}
            self.list_match_field.append(m_src_ip)
        else: 
            print "invalid src ip!"
            return 

    def onos_flow_set_dst_ip(self, dst_ip):
        from utils import ip_check
        if ip_check(dst_ip) != None:
            m_dst_ip = {"ipv4_dst":dst_ip}
            self.list_match_field.append(m_dst_ip)
        else:
            print "invalid dst ip!"
            return 

    def onos_flow_set_ethertype(self, eth_type):
        m_eth_type = {"eth_type":eth_type}
        self.list_match_field.append(m_eth_type)
        print "ethertype"

    def onos_flow_set_protocol(self, ip_proto):
        m_ip_proto = {"ip_proto":ip_proto}
        self.list_match_field.append(m_ip_proto)
        print "protocol"

    def onos_flow_set_src_port(self, src_port):
        from utils import port_check
        if port_check(src_port) != None:
            m_src_port = {"src_port":src_port}
            self.list_match_field.append(m_src_port)
        else:
            print "invalid src port"
            return

    def onos_flow_set_dst_port(self, dst_port):
        from utils import port_check
        if port_check(dst_port) != None :
            m_src_port = {"dst_port":dst_port}
            self.list_match_field.append(m_dst_port)
        else :
            print "invalid dst port"
            return

    def onos_flow_set_vlan_id(self, vlan_id):
        m_vlan_id = {"vlan_id":vlan_id}
        self.list_match_field.append(m_vlan_id)
        print "vlan_id"

    def onos_flow_set_vlan_priority(self, vlan_priority):
        m_vlan_priority = {"vlan_priority":vlan_priority}
        self.list_match_field.append(m_vlan_priority)
        print "vlan_priority"

    def onos_flow_set_tos(self, tos):
        m_tos = {"tos":tos}
        self.list_match_field.append(m_tos)
        print "tos" 
    
    def onos_flow_set_match_apply(self, dummy):
        try :
            self.make_json_flow = {
                        "flow":{
                            "action": self.instruction,
                            "priority":self.priority,
                            "match":self.list_match_field
                            },
                        "version":"1.1.0" 
                        }

        except Exception:
            traceback.print_exc()
            print "resetting!!"
        print "match_apply = ",self.make_json_flow
    
    def emptyline(self):
        """Called when an empty line is entered in response to the prompt.

        If this method is not overridden, it repeats the last nonempty
        command entered.

        """

  
    def do_flowname(self, line):
        print  self.flow_name

    def do_show(self, line):
        print self.list_match_field


    def do_match(self, line):
        attr = line.split()
        attr_len = len(attr)
        if attr_len !=0:
            try:
                if attr[0] == 'apply':     #check
                    self.match_set_func[attr[0]]('dummy')
                else:
                    self.match_set_func[attr[0]](attr[1])
            except Exception:
                traceback.print_exc()
                print "invalid argument"
        else:
            print "not appropriate implements for doing match"

    def complete_match(self, text, line, begidx, endidx):
        if not text:
            completions = self.sub_command
        else:
            completions = [f for f in self.sub_command 
                    if f.startswith(text)]
            
        return completions


    def do_priority(self, line):
        self.priority = line
        print "set priority", line

    def do_save_flow(self, line):
        from global_value import FLOW_PATH
        from utils import config_json_write
        file_path = FLOW_PATH+'/'+self.ip+'_flow.json'
        config_json_write(file_path, self.make_json_flow)
        print "saved"

    def do_send_flow(self, line):
        from onos_controller_api import onos_api_add_datapath_flows
        print self.make_json_flow
        print self.ip, self.port, self.token
        response = onos_api_add_datapath_flows(
                self.ip,
                self.port,
                self.token,
                self.dpid,
                json.dumps(self.make_json_flow),
                1)
    def do_delete_flow(self, line):
        from onos_controller_api import onos_api_delete_datapath_flows
        print self.make_json_flow
        print self.ip, self.port, self.token
        response = onos_api_delete_datapath_flows(
                self.ip,
                self.port,
                self.token,
                self.dpid,
                json.dumps(self.make_json_flow),
                1)

    def do_update_flow(self, line):
        from onos_controller_api import onos_api_update_datapath_flows
        print self.make_json_flow
        print self.ip, self.port, self.token
        response = onos_api_update_datapath_flows(
                self.ip,
                self.port,
                self.token,
                self.dpid,
                json.dumps(self.make_json_flow),
                1)


    def do_instruction(self, line):
        argc = line.split()
        action = argc[0] 
        self.instruction = action
        print "set instruction as ", self.instruction
    
    def do_exit(self, cmd_line):
        return True
    
    def do_quit(self, cmd_line):
        """Exitting"""
        os.system("figlet Good Bye!!!")
        raise SystemExit

    def complete_instruction(self, text, line, begidx, endidx):
        if not text:
            completions = self.sub_command
        else:
            completions = [f for f in self.sub_command if f.startswith(text)]
    
        return completions
    
    def complete(self, text, state):
        """Return the next possible completion for 'text'.

        If a command has not been entered, then complete against command list.
        Otherwise try to call complete_<command> to get list of completions.
        """
        if state == 0:
            import readline
            origline = readline.get_line_buffer()
            line = origline.lstrip()
            stripped = len(origline) - len(line)
            begidx = readline.get_begidx() - stripped
            endidx = readline.get_endidx() - stripped
            if begidx>0:
                cmd, args, foo = self.parseline(line)
                if cmd == '':
                    compfunc = self.completedefault
                elif cmd == 'match':
                    try:
                        line_count =  len(line.split())
                        if line_count <= 2 and begidx < len("match tos"): 
                            compfunc = getattr(self, 'complete_' + cmd)
                            self.sub_command = self.match_second_command
                        else :
                            compfunc = self.completedefault

                    except AttributeError:
                        compfunc = self.completedefault
                
                elif cmd == 'instruction':
                    try:
                        line_count =  len(line.split())
                        if begidx >= len("instruction"): 
                            compfunc = getattr(self, 'complete_' + cmd)
                            self.sub_command = self.instruction_command
                        else :
                            compfunc = self.completedefault

                    except AttributeError:
                        compfunc = self.completedefault

                else:
                    try:
                        compfunc = getattr(self, 'complete_' + cmd)
                    except AttributeError:
                        compfunc = self.completedefault
            else:
                compfunc = self.completenames
            self.completion_matches = compfunc(text, line, begidx, endidx)
        try:
            return self.completion_matches[state]
        except IndexError:
            return None    
