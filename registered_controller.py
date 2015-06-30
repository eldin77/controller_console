import os
from hp_api.hp_controller_api import *
from global_value import *

class Registered_controller(): 
    def __init__(self):
        self.controller_ip = None 
        self.controller_port = None 
        self.controller_type = "UNKNOWN Type" 

    def config_json_write(self, add_ip, add_port, con_type, c_name):
        if c_name == None:
            c_name = add_ip

        file_path = CONF_PATH+REG_CONF_FILE
        # null check 
        with open(file_path,"r") as read_file:
            json_data = json.load(read_file)
            entry = { 'name':c_name ,'ip': add_ip, 'type': con_type, 'port': str(add_port)}
            print entry
            json_data['controllers'].append(entry)
            print json_data
            read_file.close()

        with open(file_path,"w") as write_file:
            json.dump(json_data, write_file)
            write_file.close()

    def input_controller(self, argc, add_ip, add_port):
        c_name = None
        self.config_json_write(add_ip, add_port, argc[0], c_name)
    
    def search_controller(self, ip, port, c_name):
        from utils import config_json_read 
        from utils import config_json_write

        file_path = CONF_PATH+REG_CONF_FILE
        try :
            read_json = config_json_read(file_path)
            for index in range(len(read_json['controllers'])):
                if read_json['controllers'][index]['port'] == port and read_json['controllers'][index]['ip'] == ip:
                    read_json['controllers'][index]['name'] = c_name;
                    print read_json
                    config_json_write(file_path, read_json)
        
        except Exception:
            traceback.print_exc()
            return None
    
    def config_json_delete(self, c_name, json_data, index):
        file_path = CONF_PATH+REG_CONF_FILE
        try:
            del json_data['controllers'][index]
            with open(file_path,"w") as write_file:
                json.dump(json_data, write_file)
                write_file.close()
        except Exception:
            traceback.print_exc()
            print "json delete error"

    def delete_controller(self, c_name, json_data, controller_names):
        print "delete controller",c_name
        index = controller_names.index(c_name)
        self.config_json_delete(c_name, json_data, index)

