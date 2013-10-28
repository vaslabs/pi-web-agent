#!/usr/bin/python
import cgi
import cgitb
import os
cgitb.enable()
import sys
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME']+'/scripts')
sys.path.append(os.environ['MY_HOME']+'/etc/config')
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/chrome')
sys.path.append(os.environ['MY_HOME']+'/cgi-bin')
from cern_vm import Configuration
from view import View
from HTMLPageGenerator import *
from BlueprintDesigner import *
from live_info import *
import random
import crypt
import ast

class UpdateManager(object):
    def getDefaultView(self):
    
        iw_update = '<a class="btn btn-primary" ' +\
        'href="/cgi-bin/toolkit/update.py?action=update">Update</a>'
        button_bar = iw_update
        div = createDiv(button_bar, divClass='form-actions')
        update_info = update_check()

        if update_info[1] == UPDATE_PENDING:
            return '<br>Update in progress. Please try again later...'
        elif update_info[1] == REBOOT_REQUIRED:
            return '<br>No available updates. Please restart to apply previous updates.'
        elif update_info[1] != NEW_UPDATE:
            return '<br><h4>System is up to date!</h4>'

        text_area_splitted = update_info[0].split(":")
        descr_text = "<br>".join(text_area_splitted[0].split("\n"))
        
        packages_text = text_area_splitted[1].rstrip('\n')
        packages_for_update = packages_text.split(" ")
    
        packages_table_string = "<table border=\"1\"/><tr>"
        counter = 0
        for word_pack in packages_for_update[:]:
            if word_pack.isspace() or not word_pack:
                continue
            packages_table_string = packages_table_string + "<td>" + word_pack + "</td>"
            counter = counter + 1
            if counter == 5:
                counter = 0
                packages_table_string = packages_table_string + "</tr><tr>"
                
        packages_table_string = packages_table_string + "</tr></table>"
        return '<br><h5>' + descr_text + ":</h5>" + packages_table_string + div + '<br>'

    def _update(self):
        command = "sudo pi-update -a"
        [res, err] = execute(command)
        self.err=err
        return err
        
    def performUpdate(self):
        err=self._update()
        if err == UPDATE_PENDING:
            return '<br><h4>Update procedure initiated!</h4> Please come back in a moment...'
        else:
            return '<br>Something went wrong during update...<br><br>Log file: /var/log/pi_update/update.log'
            
    def checkRebootRequired():
        command = "sudo pi-update -c"
        [res, err] = execute(command)
        return err

def main():
    form = cgi.FieldStorage()
    config=Configuration()
    updMgr = UpdateManager()
    view = View(config.system.actions)
    
    if 'action' in form:       
        if form['action'].value == 'update':
            view.setContent('Update Manager', updMgr.performUpdate())
    else:
        view.setContent('Update Manager', updMgr.getDefaultView())
    view.output()
        
if __name__ == '__main__':
    main()
