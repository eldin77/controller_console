import cmd
import getpass
import logging
import S_ODLSwitch
import odl_api
import json
import logging
import odl_print

debug = True
LOG_PATH = "test.log"
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(filename=LOG_PATH, format=FORMAT)
logger = logging.getLogger('root')
if debug:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

class S_ODLController(cmd.Cmd):

    def init_call_back(self):
        self.show_all_option = {
            "switch"    : odl_api.get_switch_list,
            "host"      : odl_api.get_topology_list,
            "topology"  : odl_api.get_topology_list,
        }
        self.print_option_list = {
            "switch"    : odl_print.print_switch_list,
            "host"      : odl_print.print_host_list,
            "topology"  : odl_print.print_topology_list,
        }
        self.show_options = {
            "switch"    : odl_api.get_switch,
            "host"      : odl_api.get_host,
            "topology"  : odl_api.get_topology,
        }
        self.print_option = {
            "switch"    : odl_print.print_switch,
            "host"      : odl_print.print_host,
            "topology"  : odl_print.print_topology,
        }

    def C_Start(self, ip, port): # init odl info
        self.ip = ip
        self.port = port
        self.username = raw_input( 'username : ')
        self.password = getpass.getpass( 'password : ' )

        # odl_api login
        self.token = odl_api.login(
                                    self.ip,
                                    self.port,
                                    self.username,
                                    self.password
                                   )

        if self.token == None:
            return False

        self.controller_db = odl_api.controller_db_init(
                                                        self.ip, 
                                                        self.port, 
                                                        self.token
                                                       )
        self.init_call_back()
        self.cmdloop()

    def do_show(self, cmd_input): 
        args = cmd_input.split()
        if len(args) == 0:
            print "please input option"
            return None
        
        show_option = args[0]
        if not self.show_all_option.has_key( show_option ):
            print "invalid option"
        elif len(args) == 1:
            option_method = self.show_all_option[ show_option ]
            print_method = self.print_option_list[ show_option ]
            show_info = option_method(self.ip, self.port, self.token)
            if not show_info:
                print "fail get info"
            print_method( show_info )
            print odl_print.LINE
        elif len(args) == 2:
            pass
              
    
    def postcmd(self, stop, line):
        self.lastcmd = ''
        return stop

    def do_switch(self, cmd_input):
        args = cmd_input.split()
        if len(args) == 0:
            print "pleas input option"
            return False
        switch_name = args[0]
        sw_alias = self.controller_db["sw_alias"]
        if switch_name in sw_alias:
            dpid = sw_alias.get(switch_name)
        elif switch_name in sw_alias.values():
            dpid = switch_name
        else :
            print "switch not found"
            return False

        switch_console = S_ODLSwitch.S_ODLSwitch()
        switch_console.S_Start(self.ip, self.port, self.token, dpid)
        self.controller_db = odl_api.controller_db_init(self.ip, self.port, self.token)

    def do_alias(self, cmd_input):
        args = cmd_input.split()
        if len(args)==0:
            print "please input controller name"
        name = args[0]
        self.set_controller_alias(name)

    def set_controller_alias(self, name):
        import registered_controller
        import utils, global_value
        file_path = global_value.CONF_PATH + "/" + self.ip + ".json"
        self.controller_db['con_alias'] = name
        utils.config_json_write(file_path, self.controller_db)
        
        # registrered_controller_db write
        regi_controller = registered_controller.Registered_controller()
        regi_controller.search_controller(self.ip, self.port, name)
        self.prompt = "Controller(" + name + ") # "

    def complete_show(self, text, line, begidx, endidx):
        if not text:
            completions = self.show_options.keys()
        else :
            completions = [ x for x in self.show_options.keys()
                            if x.startswith(text)
                        ]
        return completions


    """
    def complete_switch(self, text, line, begidx, endidx):
        controller_db = odl_api.controller_db_init(self.ip, self.port, self.token)
        if not text:
            completions = list()
            for x in controller_db.get("sw_alias"):
                completions.append(x)
        else :
            completions = [x for x in controller_db.get("sw_alias").keys()
                            if x.startswith(text)
                        ]
        return 
    # TODO completion error 
    """
    
    def do_quit(self, cmd_input):
        return True
        
    def do_exit(self, cmd_input):
        return True

    def do_EOF(self, cmd_input):
        return True
 
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
                    compfunc = getattr(self, 'complete_show')
                    self.sub_command = self.show_options.keys()
                elif cmd == 'switch':
                    compfunc = getattr(self, 'complete_switch')
                    controller_db = odl_api.controller_db_init(self.ip, self.port, self.token)
                    self.sub_command = controller_db.get("sw_alias").keys()
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

if __name__ == "__main__":
    print "test"
    debug = True
    console = S_ODLController()
    console.C_Start("10.0.2.102","8181")
