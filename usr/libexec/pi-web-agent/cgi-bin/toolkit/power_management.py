#!/usr/bin/python
import sys
import os
import cgi
import cgitb

cgitb.enable()
sys.path.append(os.environ['MY_HOME']+'/cgi-bin')
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/chrome')
sys.path.append(os.environ['MY_HOME']+'/etc/config')
from HTMLPageGenerator import *
from BlueprintDesigner import *
from view import *
from cern_vm import Configuration
from framework import output

POWEROFF="poweroff"
RESTART="restart"
class PowerManager(object):
    
    def __init__(self):
        self.message="Initialised"
    
    def execute_command(self,command):
        if command==POWEROFF:
            self.shutdown()
            return True
        elif command==RESTART:
            self.restart()
            return True
        return False

    def shutdown(self):
        self.message=os.system('sudo poweroff')    
        
    def restart(self):
        self.message=os.system('sudo reboot')
            

def getView():
    
    iw_submit=InputWidget('submit', '', 'Apply Action', '', wClass='btn btn-warning')
    options=[]
    options.append({"value":POWEROFF, "text":"Shut down"})
    options.append({"value":RESTART, "text":"Restart"})
    iw_dropdown_list=DropDownListWidget('','action_list','', options, dClass='form-control select',attributes='id="select"')
    iwg = InputWidgetGroup()
    iwg.widgets=[iw_dropdown_list, iw_submit] 
    return fieldset('/cgi-bin/toolkit/power_management.py', 'GET', 'shutdown_form', iwg, createLegend("Power Options"))
    
    
def main():
    pm=PowerManager()
    fs=cgi.FieldStorage()
    config=Configuration()
    view=View(config.system.actions)
    
    if "action_list" in fs:
        
        if pm.execute_command(fs["action_list"].value):
            content="System will " + fs["action_list"].value
        else:
            content=getView()
    else:
        content=getView()
    view.setContent('Power management', content)
    
    output(view, fs)
    
if __name__ == '__main__':    
    main()
