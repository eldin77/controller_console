import cmd
import os
import traceback
from getpass import getpass
from onos_api.config_onos_switch_cmd import *

class S_ONOSController(cmd.Cmd):
   
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
        
        self.show_second_command = ["switches",
		                            "topology", 
		                            "hosts"]
        self.show_set_func = {'switches': self.switches, 
                              'topology':self.topology,
                              'hosts':self.hosts} 
   
    def C_Start(self,ip, port):
        user = raw_input("username:")
        password = getpass("password:")
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password
        self.token = None  # In future, use onos_api_login method to get token
        
        #create controller json DB
        from onos_api.onos_utils import refresh_con_db
        from global_value import CONF_PATH
        self.file_path = CONF_PATH+"/"+self.ip+".json"
        refresh_con_db(self.file_path, self.ip, self.port, self.token)
     
        os.system("figlet ONOS")
        self.cmdloop()

    def switches(self):
        from onos_api.onos_result_print import print_all_switches
        from onos_api.onos_controller_api import onos_api_switches
        from onos_api.onos_utils import return_sw_names
        
        switches_data = onos_api_switches(self.ip, self.port, self.token)
        if switches_data:
            count_switches = len(switches_data['devices'])
            for x in range(count_switches):
                try:
                    print_all_switches(switches_data,x, self.file_path)
                except KeyError:
                    print "Data not matched"
        else:
            print "No switches."

    def topology(self):
        from onos_api.onos_result_print import print_topology
        from onos_api.onos_controller_api import onos_api_topology
        topology_data = onos_api_topology(self.ip, self.port, self.token)
        if topology_data:    
            try:
                print_topology(topology_data)
            except KeyError:
                print "Data not matched"
        else:
            print "No topology informatation"
            
    def hosts(self):
        from onos_api.onos_result_print import print_hosts
        from onos_api.onos_controller_api import onos_api_hosts
        count_hosts = len(onos_api_hosts(self.ip, self.port, self.token)['hosts'])
        host_data = onos_api_hosts(self.ip, self.port, self.token)
        if host_data:
            try:
                for x in range(count_hosts):
                    print_hosts(host_data,x)
            except KeyError:
                print "Data not matched"
        else:
            print "No hosts"


    def do_show(self,cmd_line):
        if cmd_line:
            try:    
                self.show_set_func[cmd_line]()  
            except KeyError: 
                traceback.print_exc()
                print "Invalid argument"
        else:
            print "Please input an argument"
               
    def do_switch(self, cmd_line):
        from onos_api.onos_utils import return_sw_dpid
        if cmd_line:
            switch_alias = cmd_line
            switch_dpid = return_sw_dpid(self.file_path, switch_alias)
            if switch_dpid:
                command = Specific_switch_cmd()
                command.S_Start(self.ip, self.port, switch_dpid, self.token, switch_alias, self.file_path)
            else:
                print "This switch is not connected. Please press on the tab button, then select a connected switch"
        else:
            print "Please input switch name"

    def do_alias(self, cmd_line):
        from utils import config_json_read, config_json_write
        from global_value import CONF_PATH, REG_CONF_FILE

        reg_con_path = CONF_PATH+REG_CONF_FILE
        if cmd_line:
            try:
                read_con_json = config_json_read(reg_con_path)
                for controller in read_con_json['controllers']:
                    if controller['ip'] == self.ip:
                        controller['name'] = cmd_line
                        config_json_write(reg_con_path, read_con_json)

                self.prompt = cmd_line
                self.prompt = "Controller("+cmd_line+"): " 
            except Exception:
                traceback.print_exc()
                return None

    def do_quit(self, args):
        """Exitting"""
        os.system("figlet Good Bye!!!")
        raise SystemExit

    def do_exit(self, cmd_line):
        return True
    
           
    def complete_switch(self, text, line, start_index, end_index):
        if text:
            return [command for command in self.sub_command if command.startswith(text)]
        else:
            return self.sub_command
       

    def complete_show(self, text, line, start_index, end_index):
        if text: 
            return [command for command in self.sub_command if command.startswith(text)]
        else:
            return self.sub_command

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
                elif cmd == 'show':
                    compfunc = getattr(self, 'complete_' + cmd)
                    self.sub_command = self.show_second_command
                elif cmd == 'switch':
                    compfunc = getattr(self, 'complete_' + cmd)
                    from onos_api.onos_utils import return_sw_names
                    self.sub_command = return_sw_names(self.file_path)
                else:
                    try:
                        compfunc = getattr(self, 'complete_' + cmd)
                    except AttributeError:
                        #traceback.print_exc()
                        compfunc = self.completedefault

            else:
                compfunc = self.completenames
            self.completion_matches = compfunc(text, line, begidx, endidx)
        try:
            return self.completion_matches[state]
        except IndexError:
            return None
