import cmd
import traceback
from utils import *
from registered_controller import *
from hp_api.hp_controller_api import *
from hp_api.hp_result_print import *

class S_HPFlows(cmd.Cmd):
    from global_value import FLOW_PATH 
    instruction_command = ['drop', 'output']
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

    def __init__(self, completekey='tab', stdin=None, stdout=None):
        """Instantiate a line-oriented interpreter framework.

        The optional argument 'completekey' is the readline name of a
        completion key; it defaults to the Tab key. If completekey is
        not None and the readline module is available, command completion
        is done automatically. The optional arguments stdin and stdout
        specify alternate input and output file objects; if not specified,
        sys.stdin and sys.stdout are used.

        """
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
        self.instructions = []
        self.make_json_flow = {}
        self.match_funcs = [self.hp_flow_set_inport,
            self.hp_flow_set_src_mac,
            self.hp_flow_set_dst_mac,
            self.hp_flow_set_src_ip,
            self.hp_flow_set_dst_ip,
            self.hp_flow_set_ethertype,
            self.hp_flow_set_protocol,
            self.hp_flow_set_src_port,
            self.hp_flow_set_dst_port,
            self.hp_flow_set_vlan_id,
            self.hp_flow_set_vlan_priority,
            self.hp_flow_set_tos,
            self.hp_flow_set_match_apply]
        
        self.match_check_func =[]
        for x in range(len(self.match_second_command)):
            try :
                print self.match_second_command[x]
                self.match_set_func[self.match_second_command[x]] = self.match_funcs[x]
            except Exception:
                traceback.print_exc()
    
    def __call__(self, *args):
        self.ip = args[0]
        self.port = args[1]
        self.token = args[2]
        self.dpid = args[3]
        self.flow_name= args[4]
        return None

    def hp_flow_set_inport(self, in_port):
        m_in_port = {"in_port":in_port}
        self.list_match_field.append(m_in_port) 

    def hp_flow_set_src_mac(self, eth_src):
        from utils import checkmac
        checkmac(eth_src)
        m_eth_src = {"eth_src":eth_src}
        self.list_match_field.append(m_eth_src)

    def hp_flow_set_dst_mac(self, eth_dst):
        from utils import checkmac
        checkmac(eth_dst)
        m_eth_dst = {"eth_dst":eth_dst}
        self.list_match_field.append(m_eth_dst)

    def hp_flow_set_src_ip(self, src_ip):
        from utils import ip_check
        if ip_check(src_ip) != None:
            m_src_ip = {"ipv4_src":src_ip}
            self.list_match_field.append(src_ip)
        else: 
            print "invalid src ip!"
        return 

    def hp_flow_set_dst_ip(self, dst_ip):
        from utils import ip_check
        if ip_check(dst_ip) != None:
            m_dst_ip = {"ipv4_dst":dst_ip}
            self.list_match_field.append(dst_ip)
        else:
            print "invalid dst ip!"
        return 

    def hp_flow_set_ethertype(self, eth_type):
        m_eth_type = {"eth_type":eth_type}
        self.list_match_field.append(m_eth_type)
        print "ethertype"

    def hp_flow_set_protocol(self, ip_proto):
        m_ip_proto = {"ip_proto":ip_proto}
        self.list_match_field.append(m_ip_proto)
        print "protocol"

    def hp_flow_set_src_port(self, src_port):
        from utils import port_check
        if port_check(src_port) != None:
            m_src_port = {"src_port":src_port}
            self.list_match_field.append(m_src_port)
        else:
            print "invalid src port"
        return

    def hp_flow_set_dst_port(self, dst_port):
        from utils import port_check
        if port_check(dst_port) != None :
            m_src_port = {"dst_port":dst_port}
            self.list_match_field.append(m_dst_port)
        else :
            print "invalid dst port"
        return

    def hp_flow_set_vlan_id(self, vlan_id):
        m_vlan_id = {"vlan_id":vlan_id}
        self.list_match_field.append(m_vlan_id)
        print "vlan_id"

    def hp_flow_set_vlan_priority(self, vlan_priority):
        m_vlan_priority = {"vlan_priority":vlan_priority}
        self.list_match_field.append(m_vlan_priority)
        print "vlan_priority"

    def hp_flow_set_tos(self, tos):
        m_tos = {"tos":tos}
        self.list_match_field.append(m_tos)
        print "tos" 
    
    def hp_flow_set_match_apply(self, dummy):
        try :
            self.make_json_flow = {
                    "flow":{
                        "actions": [self.instructions],
                        "priority":self.priority,
                        #"idle_timeout": self.idle_timeout,
                        "match":self.list_match_field
                        },
                    "version":"1.0.0" 
                    }

        except Exception:
            traceback.print_exc()
            print "resetting!!"
        print "match_apply = ",self.make_json_flow
        #write_json_file

    def emptyline(self):
        """Called when an empty line is entered in response to the prompt.

        If this method is not overridden, it repeats the last nonempty
        command entered.

        """
        #if self.lastcmd:
        #    print "emptyline"
        #    return self.onecmd(self.lastcmd)

    def do_quit(self, line):
        return True

    def do_exit(self, line):
        return True

    def do_flowname(self, line):
        print "change_flow_name"
    
    def do_show(self, line):
        print self.list_match_field

    def do_match(self, line):
        attr = line.split()
        attr_len = len(attr)
        if attr_len != 0:
            try:
                #check line
                if attr[0] == 'apply':
                    self.match_set_func[attr[0]]('dummy')
                else :
                    self.match_set_func[attr[0]](attr[1])
            except Exception:
                traceback.print_exc()
                print "invalid argment"
        else :
            print "not implements do match"

    def complete_match(self, text, line, begidx, endidx):
        if not text:
            completions = self.sub_command
        else:
            completions = [f for f in self.sub_command
                    if f.startswith(text)]

        return completions

    def complete_instructions(self, text, line, begidx, endidx):
        if not text:
            completions = self.sub_command
        else:
            completions = [f for f in self.sub_command
                    if f.startswith(text)]

        return completions

    def do_priority(self, line):
        self.priority = line
        print "set priority",line
    
    def do_save_flow(self, line):
        from utils import config_json_write
        file_path = FLOW_PATH+'/'+self.flow_name 
	config_json_write(file_path, self.make_json_flow)
        print "save"

    def do_send_flow(self, line):
        from hp_api.hp_controller_api import hp_api_add_datapath_flows
        print self.make_json_flow
        print self.ip, self.port, self.token
        response = hp_api_add_datapath_flows(self.ip, self.port, self.token, self.dpid, json.dumps(self.make_json_flow),1)
    def do_load_flow(self, line):
        print "load"

    def do_instructions(self, line):
        #check_action
        split_line = line.split()
        action = {split_line[0]:int(split_line[1])}
        self.instructions = action

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
                
                elif cmd == 'instructions':
                    try:
                        line_count =  len(line.split())
                        if begidx >= len("instructions"): 
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
