import cmd
import traceback
import getpass
from registered_controller import *
from hp_api.hp_controller_api import *
from hp_api.hp_result_print import *
from hp_api.config_hp_switch_cmd import *

class S_HPController(cmd.Cmd):

    show_second_command = ['switch','version'] 
    show_third_command = ['flows','ports']
    hp_mac_db = []
    hp_sw_alias_db = []

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
        
        self.ip = str()
        self.port = int() 
        self.user = str()
        self.password = str()
        self.controller_uid = str()
        self.token = []
        self.dpids = []
        self.sw_alias = []
        self.org_dpids = {}
        self.sw_alias_tuple = {}
        
        self.switch_show_func = {'flows':hp_api_get_datapath_flows,
                                 'ports':hp_api_get_datapath_port}

        self.switch_func = {'switch': self.show_switch,
                            'version':self.show_version}

        self.sub_command = self.show_second_command

    def __call__(self, *args):
        self.ip = args[0]
        self.port = args[1]
        self.token = args[2]
        self.refresh_dpid_list()
        self.init_value()
    
    def refresh_dpid_list(self):
        self.dpids = []
        try:
            dpid_res = hp_api_get_datapaths(self.ip, self.port, self.token)
            datapath_count = len(dpid_res['datapaths'])
            for x in range(datapath_count):
                tmp_dpids = json.dumps(dpid_res['datapaths'][x]['dpid'])
                sec_tmp_dpids = "".join(tmp_dpids.split(":"))
                the_tmp_dpids = sec_tmp_dpids.split('"') 
                self.dpids.append(the_tmp_dpids[1])
                self.org_dpids[the_tmp_dpids[1]] = tmp_dpids
        except Exception:
            traceback.print_exc()

    def controller_all_config(self):
        response = hp_api_stats(self.ip, self.port, self.token, 1)
        response = hp_api_ports(self.ip, self.port, self.token, 0)
        response = hp_api_version(self.ip, self.port, self.token, 1)
        try:
            dpid_res = hp_api_get_datapaths(self.ip, self.port, self.token)
            datapath_count = len(dpid_res['datapaths'])
            for x in range(datapath_count):
                tmp_dpids = json.dumps(dpid_res['datapaths'][x]['dpid'])
                hp_api_get_datapath_port(self.ip, self.port, self.token, tmp_dpids, 0)
                #hp_api_get_datapath_flows(ip, port, token, tmp_dpids)
        except Exception:
            traceback.print_exc()

    def get_token(self, ip, port, user ,password):
        token = hp_api_login(str(ip), int(port), user, password) 
        if token == None:
            print "login fail reconnection plz"
            raise ValueError
        return token

    def C_Start(self, ip, port):
        user = raw_input("user :")
        password = getpass.getpass("password :")
        
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password

        try :
            token = self.get_token(ip, port, user, password)
        except Exception:
            traceback.print_exc()
            return False

        self.token = token['token']
        self.controller_all_config()
        self.init_value()
        self.cmdloop()

    def show_version(self, attr, attr_len):
        version_res = hp_api_version(str(self.ip), int(self.port), self.token, 1)

    def do_show(self, cmd_line):
        from hp_api.hp_controller_api import show_openflow_switch_info
        from utils import sw_alias_db 
        attr = cmd_line.split()
        attr_len = len(attr)

        if attr_len != 0:
            try:
                self.switch_func[attr[0]](attr, attr_len) 
            except Exception:
                print "not implements!!"

    def init_value(self):
        from utils import refresh_alias_json_db
        from utils import mac_db 
        from utils import sw_alias_db 
        self.sw_alias = []

        self.controller_uid = refresh_alias_json_db(self.ip, self.port, self.token, None, None)
        self.hp_mac_db = mac_db
        self.hp_sw_alias_db = sw_alias_db 

        for sw_list in self.hp_sw_alias_db:
            tmp_sw_list = self.hp_sw_alias_db[sw_list]
            self.sw_alias_tuple[tmp_sw_list] = sw_list
            self.sw_alias.append(tmp_sw_list)

    def emptyline(self):
        """Called when an empty line is entered in response to the prompt.

        If this method is not overridden, it repeats the last nonempty
        command entered.

        """
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
                #print "cmd = ",cmd ,"args = ",args ,foo
                #print "orig = ",origline, "line =",line, "stripped = ", stripped
                if cmd == '':
                    compfunc = self.completedefault
                elif cmd == 'show':
                    compfunc = getattr(self, 'complete_' + cmd)
                    self.sub_command = self.show_second_command
                    #compfunc = self.completedefault

                    split_args = args.split()
                    try :
                        if split_args[0] == 'switch' and begidx == 12:
                            self.sub_command = self.sw_alias
                            #self.sub_command = self.dpids
                        elif split_args[0] == 'switch' and len(split_args) >= 2:
                            self.sub_command = self.show_third_command
                        else:
                            self.sub_command = self.show_second_command
                    except Exception:
                        #traceback.print_exc()
                        self.sub_command = self.show_second_command

                elif cmd == 'switch':
                    compfunc = getattr(self, 'complete_' + cmd)
                    self.sub_command = self.sw_alias
                else:
                    try:
                        compfunc = getattr(self, 'complete_' + cmd)
                    except Exception:
                        #traceback.print_exc()
                        compfunc = self.completedefault

            else:
                compfunc = self.completenames
            self.completion_matches = compfunc(text, line, begidx, endidx)
        try:
            return self.completion_matches[state]
        except IndexError:
            return None

    def do_quit(self, line):
        exit() 

    def do_exit(self, line):
        return True

    def complete_show(self, text, line, begidx, endidx):
        if not text:
            completions = self.sub_command
        else:
            completions = [f for f in self.sub_command
                    if f.startswith(text)]

        return completions

    def complete_switch(self, text, line, begidx, endidx):
        if not text:
            completions = self.sub_command
        else:
            completions = [f for f in self.sub_command
                    if f.startswith(text)]

        return completions

    def check_datapath(self, datapath):
        try:
            index = self.dpids.index(datapath)
        except Exception:
            traceback.print_exc()
            return None 

        return None 

    def check_datapath_alias(self, cmd_line):
        try:
            tmp_check_alias = self.sw_alias_tuple[cmd_line]
            check_alias =  "".join(json.dumps(tmp_check_alias).split(":"))
            return check_alias.split('"')[1]
        except Exception:
            traceback.print_exc()
            return None

        return None

    def show_switch(self, attr, attr_len):
        from hp_api.hp_controller_api import show_openflow_switch_info
        from utils import sw_alias_db 
        if attr_len == 1:
            try :
                dpid_res = hp_api_get_datapaths(self.ip, self.port, self.token)
                datapath_count = len(dpid_res['datapaths'])
                self.refresh_dpid_list()
                for x in range(datapath_count):
                    sw_name = sw_alias_db[dpid_res['datapaths'][x]['dpid']]
                    print_datapaths(dpid_res['datapaths'][x], sw_name)
            except Exception:
                traceback.print_exc()

        elif attr_len == 2:
            change_data = self.check_datapath_alias(attr[1])
            #print change_data 
            if change_data == None:
                print "invalid DPID!!"
            else :
                #dpid = self.org_dpids[attr[1]]
                dpid = self.org_dpids[change_data].split('"')[1]
                #split_dpid = dpid.split('"')
                sw_name = sw_alias_db[dpid]
                show_openflow_switch_info(self.ip, self.port, self.token, sw_name, dpid, 1)

        elif attr_len == 3:
            try:
                dpid = self.org_dpids[attr[1]].split('"')
                self.switch_show_func[attr[2]](self.token,dpid[1])
            except Exception:
                traceback.print_exc()
                print "invalid argment"
        else:
            print "to many argment"
    
    def do_switch(self, cmd_line):
        change_data = self.check_datapath_alias(cmd_line)
        #if (self.check_datapath(cmd_line)):
        if change_data == None:
            print "invalid DPID!!"
        else:
            cmdline = S_HPSwitch()
            cmdline(self.ip, self.port, 
                    self.token, self.sw_alias_tuple[cmd_line], 
                    cmd_line)
            cmdline.prompt = "Controller("+cmd_line+"): " 
            cmdline.cmdloop()
        self.init_value()

    def do_alias(self, cmd_line):
        from utils import refresh_alias_json_db
        from utils import config_json_write
        from utils import config_json_read
        from global_value import CONF_PATH 
        
        reg_cont = Registered_controller()
        file_path = CONF_PATH+"/"+self.controller_uid+".json"
        try :
            read_json = config_json_read(file_path)
            read_json['controllers']['con_alias'] = cmd_line
            config_json_write(file_path, read_json)
            refresh_alias_json_db(self.ip, self.port, self.token, None, None)
            self.prompt = cmd_line
            self.prompt = "Controller("+cmd_line+"): " 
            reg_cont.search_controller(self.ip, self.port, cmd_line)

        except Exception:
            traceback.print_exc()
            return None
