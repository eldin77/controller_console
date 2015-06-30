import cmd
import traceback
from registered_controller import *
from hp_api.hp_controller_api import *
from hp_api.hp_result_print import *
from hp_api.config_hp_flows_cmd import *

class S_HPSwitch(cmd.Cmd):

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
            self.sw_name = str()

    def __call__(self, *args):
        from utils import mac_db 
        from utils import sw_alias_db 
        from utils import g_controller_uid 
        from utils import refresh_alias_json_db
        from hp_controller_api import show_openflow_switch_info

        self.ip = args[0]
        self.port = args[1]
        self.token = args[2]
        self.dpid = args[3]
        self.sw_name = args[4]

        self.controller_uid = refresh_alias_json_db(self.ip, self.port, self.token, None, None)
        self.hp_mac_db = mac_db
        self.hp_sw_alias_db = sw_alias_db

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

    def do_show(self, line):
        print "static_flows_do_show",line
        show_openflow_switch_info(self.ip, self.port, self.token, self.sw_name, self.dpid,1)

    def do_alias(self, line):
        from utils import refresh_alias_json_db
        from utils import config_json_read 
        from utils import config_json_write
        from global_value import CONF_PATH 
        #read and mode and write json db
        file_path = CONF_PATH+"/"+self.controller_uid+".json"
        try :
            read_json = config_json_read(file_path)
            for dpid_list in read_json['controllers']['switchs']:
                if dpid_list['dpid'] == self.dpid:
                    #line command check
                    dpid_list['sw_alias'] = line
                    print "change switch alias"
                    break
            print self.hp_sw_alias_db
            config_json_write(file_path, read_json)
            refresh_alias_json_db(self.ip, self.port, self.token, None, None)
            self.sw_name = line
        except Exception:
            traceback.print_exc()
            return None

        #check line
        self.prompt = "Controller("+line+"): " 
        print "change datapath name",line

    def check_cmdline(self, cmd_line):
        cmd_len = len(cmd_line.split())
        if cmd_len > 2:
            print "flows name error 1 argement plz"
            return True
        else :
            print "check ok"
        return None 

    def do_flows(self, line):
        if (self.check_cmdline(line)):
            print "invalid cmdline!!"
        else:
            print line
            cmdline = S_HPFlows()
            cmdline(self.ip, self.port, self.token, self.dpid, line)
            cmdline.prompt = "Controller(flows:"+line+"): " 
            cmdline.cmdloop()

            print "do_flows",line

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
                elif cmd == 'flows':
                    try:
                        compfunc = getattr(self, 'complete_' + cmd)
                    except AttributeError:
                        compfunc = self.completedefault
                
                elif cmd == 'alias':
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
