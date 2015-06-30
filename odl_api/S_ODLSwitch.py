import cmd
import odl_api
import odl_print
import global_value
import utils
import S_ODLFlow

class S_ODLSwitch(cmd.Cmd): 
    def do_quit(self, cmd_input):
        return True

    def do_exit(self, cmd_input):
        return True

    def do_EOF(self, cmd_input):
        return True

    def S_Start(self, ip, port, token, dpid):
        self.ip = ip
        self.port = port
        self.token = token
        self.dpid = dpid
        self.init_call_back()
        
        # switch info print 
        switch_info = odl_api.get_switch(self.ip, self.port, self.token, self.dpid)
        odl_print.print_switch(switch_info)
        print odl_print.LINE

        # switch alias load
        controller_db = odl_api.controller_db_init(ip, port, token)
        sw_alias_db = controller_db["sw_alias"]
        self.alias = odl_api.find_alias_in_dpid(self.dpid, sw_alias_db)
        controller_db.clear()
        self.prompt = "Switch(" + self.alias + ") # "

        # console start
        self.cmdloop()

    def postcmd(self, stop, line):
        self.lastcmd = ""
        return stop

    def init_call_back(self):
        self.show_option = {
            "port"  :   odl_api.get_switch_port_list,
            "flow" :   odl_api.get_switch_flow_list,
        }
        self.print_option = {
            "port"  :   odl_print.print_switch_port_list,
            "flow"  :   odl_print.print_switch_flow_list,
        }

    def do_show(self, cmd_input):
        args = cmd_input.split()
        if len(args) == 0:
            print "please input option"
            return None
        input_option = args[0]
        if not self.show_option.has_key(input_option): # args[0] is input option
            print "invalid input option"
            return None
        else :
            option_method = self.show_option[input_option]
            print_method = self.print_option[input_option]
            show_info = option_method(self.ip, self.port, self.token, self.dpid)
            print_method(show_info)
            print odl_print.LINE

    def do_alias(self, cmd_input):
        args = cmd_input.split()
        if len(args) == 0:
            print "pleas input option"
        input_alias = args[0]
        if self.alias == input_alias:
            print "alias is same"
        else :
            self.set_alias(args[0])

    def set_alias(self, input_alias):
        file_path = global_value.CONF_PATH +"/" + self.ip + ".json"
        controller_db = utils.config_json_read(file_path)
        sw_alias_db = controller_db["sw_alias"]
        temp_dpid = sw_alias_db.get(input_alias)
        if temp_dpid:
            yn = "you want replace \"" + input_alias + "\":\"" + temp_dpid + "\" -> \"" + input_alias + "\":\"" + self.dpid + "\" ? (y/n) # "
            if not yn.lower() == "y" :
                print "cancle replace"
                return None
            sw_alias_db[temp_dpid] = temp_dpid

        sw_alias_db.pop(self.alias)
        sw_alias_db[input_alias] = self.dpid
            

        
        utils.config_json_write(file_path, controller_db)
        self.prompt = "Switch(" + input_alias + ") # "

    def do_flow(self, cmd_input):
        args = cmd_input.split()
        if len(args) == 0:
            print "please input option"
            return None
        else:
            flow_id = args[0]
            flow_console = S_ODLFlow.S_ODLFlow()
            flow_console.F_Start(self.ip, self.port, self.token, self.dpid, flow_id)

    def complete_show(self, text, line, begidx, endidx):
        if not text:
            completions = self.show_option.keys()
        else:
            completions = [x for x in self.show_option.keys()
                            if x.startswith(text)
                        ]
        return completions


if __name__ == "__main__":
    debug = True
    token = odl_api.login('10.0.2.102','8181','admin','admin')
    console = S_ODLSwitch()
    console.S_Start("10.0.2.102","8181",token,"openflow:515")

