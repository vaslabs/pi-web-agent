#!/usr/bin/python
import os
import json

CONFIG_FILE=os.environ['MY_HOME']+"/etc/config/config.cfg"
CONFIG_PATH=os.environ['MY_HOME']+"/etc/config"
VERSION="0.4-rc-2"
class Configuration(object):
    
    def __init__(self):
        json_file = open(CONFIG_FILE)
        self.config=json.load(json_file)
        json_file.close()
        system=self.config['pi-web-agent']['system']
        actions = system['actions']
        self.system=System()
        self.system.actions = actions
        try:
            extensionFile=system['extension']
            json_file = open(CONFIG_PATH+'/'+extensionFile)
            extension = json.load(json_file)
            json_file.close()
            cmd_actions = extension['pi-web-agent']['actions']
            self.system.cmdactions = cmd_actions
        except:
            pass
            
class System(object):
    
    def __init__(self):
        self.actions=None
        self.cmdactions=None
        

    
