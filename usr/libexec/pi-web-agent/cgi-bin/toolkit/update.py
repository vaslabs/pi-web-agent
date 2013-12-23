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
from view import View
from HTMLPageGenerator import *
from BlueprintDesigner import *
from live_info import *
from framework import view

def parse_package_name(package_entry):
    package_elements=package_entry.split()
    for element in package_elements[1:]:
        if (len(element) > 1):
            return element
    return None
    
def parse_package_description(package_entry):
    package_elements=package_entry.split()
    counter=0
    for element in package_elements:
        if (len(element) > 1):
            break
        counter+=1
    counter += 2
    description=""
    for element in package_elements[counter:]:
        description+=element + " "
    return description
                
class UpdateManager(object):
    
    def getDefaultView(self):
    
        iw_update = '<a class="btn btn-primary" ' +\
        'href="/cgi-bin/toolkit/update.py?action=update">Update</a>'
        button_bar = iw_update
        div = createDiv(button_bar, divClass='form-actions')
        update_info, returncode = update_check_quick()

        if returncode == UPDATE_PENDING:
            return '<br>Update in progress. Please try again later...'
        elif returncode == REBOOT_REQUIRED:
            return '<br>Reboot is required to apply previous updates.'
        elif returncode == UPDATE_READY or returncode == NO_ACTION:
            return '<br><h4>System is up to date!</h4>'
        elif returncode != NEW_UPDATE:
            return '<br><h4>Warning: Last update was interrupted!</h4>\n'+\
                '<br><h5>Recovery procedure initiated. Please come back in a moment...</h5>'
        
        packages_table_string = "<table border=\"1\"/><tr>"
        for package_entry in update_info.split("\n"):
            package_name=parse_package_name(package_entry)
            if package_name == None:
                continue
            description=parse_package_description(package_entry)
            packages_table_string += "<td>" + package_name + "</td>" +\
            "<td>"+description+"</td>"
            packages_table_string += "</tr><tr>"
                
        packages_table_string = packages_table_string + "</tr></table>"
        descr_text='<h4>'+str(len(update_info.split("\n")) - 1) + " updates are available!</h4>"
        return '<br><h5>' + descr_text + "</h5>" + packages_table_string + div + '<br>'

    def _update(self):
        command = "sudo pi-update -a"
        err = os.system(command)
        self.err=err
        return err
        
    def performUpdate(self):
        err = self._update()
        if err == DPKG_CONFIG_NEEDED:
            return '<br><h4>Warning: Last update was interrupted!</h4>\n'+\
                '<br><h5>Recovery procedure initiated. Please come back in a moment...</h5>'
        else:
            return '<br><h4>Update procedure initiated!</h4> Please come back in a moment...'
    
def main():
    form = cgi.FieldStorage()
    updMgr = UpdateManager()

    if 'action' in form:       
        if form['action'].value == 'update':
            view.setContent('Update Manager', updMgr.performUpdate())
    else:
        view.setContent('Update Manager', updMgr.getDefaultView())
    view.output()
        
if __name__ == '__main__':
    main()
