#!/usr/bin/python
import sys
import os
import cgi
import cgitb

cgitb.enable()
sys.path.append(os.environ['MY_HOME']+'/cgi-bin')
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/chrome')
sys.path.append(os.environ['MY_HOME']+'/etc/config')
from framework import output, view
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
    
    return "Obsolete call"
    
def main():
    pm=PowerManager()
    fs=cgi.FieldStorage()
    
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
