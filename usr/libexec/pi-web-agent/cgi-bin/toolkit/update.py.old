#!/usr/bin/python
import cgi
import cgitb
import os
cgitb.enable()
import sys
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/cernvm-appliance-agent'
sys.path.append(os.environ['MY_HOME']+'/scripts')
sys.path.append(os.environ['MY_HOME']+'/etc/config')
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/chrome')
sys.path.append(os.environ['MY_HOME']+'/cgi-bin')
from cern_vm import Configuration
from view import View
from HTMLPageGenerator import *
from BlueprintDesigner import *
import random
import crypt
import ast
from live_info import *

class UpdateManager(object):

    def getDefaultView(self):
        iw_update = '<a class="btn btn-primary" ' +\
        'href="/cgi-bin/toolkit/update.py?action=update">Update</a>'
        button_bar = iw_update
        div=createDiv(button_bar, divClass='form-actions')
        update_info=update_check_with_version()
        if update_info[0]:
            return 'Updates are available<br>' + div 
        else:
            return '<h3>System is up to date</h3><br>Version: ' + update_info[1]

    def _update(self):
        command = "sudo cernvm-update -a"
        [res, err]=execute(command)
        self.err=err
        return err

    def doTransaction(self):
        err=self._update()
        if  err == UPDATE_READY:
            return self.getUpdatedView()
        else:
            return self.getDefaultView()

    def getUpdatedView(self):
        iw_reboot = '<a class="btn btn-primary" ' +\
        'href="/cgi-bin/toolkit/power_management?action_list=restart">Reboot</a>'
        button_bar = iw_reboot
        div=createDiv(button_bar, divClass='form-actions')
        return 'A restart is required to apply updates<br>' + div    

    

def main():
    form = cgi.FieldStorage()
    config=Configuration()
    updMgr = UpdateManager()
    view = View(config.system.actions)
    
    if 'action' in form:       
        if form['action'] == 'update':
            view.setContent('Update Manager', updMgr.doTransaction())
    else:
        view.setContent('Update Manager', updMgr.getDefaultView())
    view.output()
        
if __name__ == '__main__':
    main()
