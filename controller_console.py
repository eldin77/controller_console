import cmd
import traceback
from utils import *
from registered_controller import *
from hp_api.hp_controller_api import *
from hp_api.hp_result_print import *
from hp_api.config_hp_cmd import *
from hp_api.config_hp_switch_cmd import *
from onos_api.config_onos_cmd import *
from odl_api.S_ODLController import *

PROMPT = 'Controller# '

class SDNControllerConsole(cmd.Cmd):
    

    prompt = PROMPT
    controllers = []
    controller_names = [] 
    controller_count = int()
    file_path = str()
    add_controller_help = ['add <type> <ip> <port>']
    CONTROLLERS_TYPE = ['HP','ODL','ONOS']

    con_type = {
            'HP':0,
            'ODL': 0, 
            'ONOS': 0
            }

    controller_type = {
            'HP':S_HPController(),
            'ODL': S_ODLController(),
            'ONOS':S_ONOSController(),
            }

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

        self.file_path = CONF_PATH+REG_CONF_FILE
        self.controllers = get_controller_conf(self.file_path)
        self.controller_count = len(self.controllers['controllers'])
        for x in range(self.controller_count):
            tmp_name = self.controllers['controllers'][x]['name']
            name = json.dumps(tmp_name).replace('"',"")
            self.controller_names.append(name)

    def refresh_controller_list(self):
        self.controller_names = []
        self.controllers = get_controller_conf(self.file_path)
        self.controller_count = len(self.controllers['controllers'])
        for x in range(self.controller_count):
            tmp_name = self.controllers['controllers'][x]['name']
            name = json.dumps(tmp_name).replace('"',"")
            self.controller_names.append(name)

    def emptyline(self):
        """Called when an empty line is entered in response to the prompt.

        If this method is not overridden, it repeats the last nonempty
        command entered.

        """
        #if self.lastcmd:
        #    print "emptyline"
        #    return self.onecmd(self.lastcmd)

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
                    try:
                        compfunc = getattr(self, 'complete_' + cmd)
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

    def do_show(self, cmd_line):
        self.refresh_controller_list()
        attr = cmd_line.split()
        attr_len = len(attr)
        if attr_len != 0:
            if attr[0] == 'all':
                for x in range(self.controller_count):
                    try:
                        print_controller_list(self.controllers['controllers'][x])
                    except Exception:
                        traceback.print_exc()
                        print "All Error Not Found Controller"
                        return None

            elif attr_len < 2 and attr_len > 0:
                try:
                    index = self.controller_names.index(attr[0]) 
                    print_controller_list(self.controllers['controllers'][index])
                except Exception:
                    traceback.print_exc()
                    print "Single Error Not Found Controller"
                    return None
        #hp_api_login()
        #print cmd_line

    def do_delete(self, cmd_line):
        self.refresh_controller_list()
        argc = cmd_line.split()
        args = len(argc)
        if args > 1 or args == 0:
            print "arguments delete <controller_name>"
            return None
        else:
            del_cont = Registered_controller()
            try:
                index = self.controller_names.index(argc[0])
                del_cont.delete_controller(argc[0],self.controllers, self.controller_names)
                self.refresh_controller_list()
            except Exception:
                traceback.print_exc()
                print "No Search Controller Delete Error"
        return None

    def do_add(self, cmd_line):
        reg_cont = Registered_controller()
        argc = cmd_line.split()
        args = len(argc)

        if 2 < args :
            #type check
            try:
                self.con_type[argc[0]] += 1
               #print self.con_type[argc[0]]
            except Exception:
                traceback.print_exc()
                print self.add_controller_help 
                return None
            #ip check     
            ip = ip_check(argc[1])
            if ip != None:
                add_ip = argc[1] 
            else:
                print "ip value error"
                print self.add_controller_help
                return None
            #port check 
            try:
                port = port_check(int(argc[2]))
                if port != None:
                    add_port = port 
                else:
                    print self.add_controller_help
                    return None

            except Exception: 
                traceback.print_exc()
                print "port value error"
                print self.add_controller_help

            reg_cont.input_controller(argc, add_ip, add_port)
            self.refresh_controller_list()

        else:
            print "arguments error" 
            print self.add_controller_help 
    
    def do_config(self, cmd_line):
        attr = cmd_line.split()
        try:
            index = self.controller_names.index(attr[0])
            cont_type = self.controllers['controllers'][index]['type']
            ip = self.controllers['controllers'][index]['ip']
            port = self.controllers['controllers'][index]['port']
        except Exception:
            traceback.print_exc()
            print "Single Error Not Found Controller"
            return None

        try: 
            cmdline = self.controller_type[cont_type]
            cmdline.prompt = "Controller("+cmd_line+"): " 
            cmdline.C_Start(ip, port)
            self.refresh_controller_list()
        except Exception:
            traceback.print_exc()
            print "error"
       # return True

    def do_quit(self, line):
        print "bye bye~~ see you again"
        return True

    def do_exit(self, line):
        print "bye bye~~ see you again"
        return True

    def do_prompt(self, line):
        print "Change the interactive prompt"
        self.prompt = line + ': '

    def complete_show(self, text, line, begidx, endidx):
        if not text:
            #completions = self.controllers['controllers'].keys()
            completions = self.controller_names
        else:
            #completions = [f for f in self.controllers['controllers'].keys()
            completions = [f for f in self.controller_names
                    if f.startswith(text)
                    ]
        return completions

    def complete_config(self, text, line, begidx, endidx):
        if not text:
            #completions = self.controllers['controllers'].keys()
            completions = self.controller_names
        else:
            #completions = [f for f in self.controllers['controllers'].keys()
            completions = [f for f in self.controller_names
                    if f.startswith(text)
                    ]
        return completions

    def complete_delete(self, text, line, begidx, endidx):
        line_len = len(line.split())
        limit_line_count = 2
        if line_len >= limit_line_count and not text:
            completions = None
        else :
            if not text:
                #completions = self.controllers['controllers'].keys()
                completions = self.controller_names
            else:
                #completions = [f for f in self.controllers['controllers'].keys()
                completions = [f for f in self.controller_names
                        if f.startswith(text)
                        ]
        return completions

    def complete_add(self, text, line, begidx, endidx):
        if not text:
            completions = self.CONTROLLERS_TYPE
        else:
            completions = [f for f in self.CONTROLLERS_TYPE
                    if f.startswith(text)
                    ]
        return completions

    def complete_show_attr(self, text, line, begidx, endidx):
        if not text:
            completions = self.SWITCHS[:]
        else:
            completions = [f for f in self.SWITCHS 
                    if f.startswith(text)
                    ]
        return completions


if __name__ == '__main__':
    cmdline = SDNControllerConsole()
    cmdline.cmdloop()
