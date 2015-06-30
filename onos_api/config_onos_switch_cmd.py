import cmd
import traceback
import urllib2
import json
import os
from onos_api.config_onos_flows_cmd import *

class Specific_switch_cmd(cmd.Cmd):
	
    def S_Start(self, ip, port, sw_dpid, token,  switch_alias, file_path):
        self.ip = ip
        self.port = port
        self.sw_dpid = sw_dpid
        self.token = token
        self.switch_alias = switch_alias
        self.file_path =file_path
        print "Entering to "+self.switch_alias
        from onos_api.onos_controller_api import onos_api_specific_switch
        from onos_api.onos_result_print import print_specific_switch
        specific_switch_data = onos_api_ports(self.ip, self.port, self.sw_dpid, self.token)   
        if specific_switch_data:
            try:
                print_specific_switch(specific_switch_data, self.file_path)
                self.prompt = "#switch("+self.switch_alias+"):"
                self.cmdloop()
            except KeyError:
                print "Data not matched"
        else:
            print "This switch is disconnected"
	
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

        self.switch_show_complete_methods = ["ports",
		                                     "flows"]
        self.switch_show_set_func = {'ports':self.ports,
                                     'flows':self.flows}

    def ports(self):
        from onos_api.onos_result_print import print_ports
        from onos_api.onos_controller_api import onos_api_ports
        port_data = onos_api_ports(self.ip, self.port, self.sw_dpid, self.token)
        if port_data:
            count_port = len(port_data['ports'])
            for x in range(count_port):
                try:
                    print_ports(port_data, x)
                except KeyError:
                    traceback.print_exc()
                    print "Data not matched"
                    return None
        else:
            print "No port information"

    def flows(self):
        from onos_api.onos_result_print import print_specific_switch_flow
        from onos_api.onos_controller_api import onos_api_flows
        flow_data = onos_api_flows(self.ip, self.port, self.sw_dpid, self.token)
        if flow_data:
            count_flow = len(flow_data['flows'])
            for x in range(count_flow):
                try:
                    print_specific_switch_flow(flow_data, x)
                except KeyError:
                    traceback.print_exc()
                    print "Print function call error"
                    return None
        else:
            print "No flow information"

    def do_show(self, cmd_line):
        if cmd_line:
            try:
                self.switch_show_set_func[cmd_line]()
            except KeyError:
                traceback.print_exc()
                print "Invalid argument"
        else:
            print "Please choose an argument (press on the tab key)"

                   
    def complete_show(self, text, line, start_index, end_index):
        show_sub = ["ports", "flows"]
        if not text:
            completions = show_sub
        else:
            completions = [command for command in show_sub if command.startswith(text)]
        return completions

    def do_alias(self, cmd_line):        	
        from utils import config_json_read, config_json_write
        from onos_api.onos_utils import return_sw_names
        if cmd_line:
            switch_names = return_sw_names(self.file_path)
            if cmd_line in switch_names:
                print"Duplicated name, please input another name!!!"
            else:
                try:
                    switches = config_json_read(self.file_path)
                    switches[self.sw_dpid] = cmd_line
                    config_json_write(self.file_path, switches)
                    self.prompt = "#switch("+cmd_line+"): " 
                except Exception:
                    traceback.print_exc()
                    return None
        else:
            print "Please input switch alias"

           
    def do_flow(self, cmd_line):       #flow name return                       
        if cmd_line:
            flow = S_ONOSFlows()
            flow(self.ip, self.port, self.token, self.sw_dpid, cmd_line)
            flow.prompt = "#switch("+self.switch_alias+"("+cmd_line+")):"
            flow.cmdloop()
            print "Create a flow", cmd_line
        else:
            print "Please give a flow name"
            

    def do_exit(self, line):
		return True

    def do_quit(self, args):
        """Exitting"""
        os.system("figlet Good Bye!!!")
        raise SystemExit


