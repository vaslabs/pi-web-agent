#!/usr/bin/python

import json
import os, sys
from live_info import *
import cgi, cgitb
cgitb.enable()
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME'] + '/etc/config')

from HTMLPageGenerator import composeJS
from framework import view, output
from functools import partial
import re
import subprocess


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


def get_packages():
    packages = list()
    update_info, returncode = update_check_quick()

    if returncode in (UPDATE_PENDING, REBOOT_REQUIRED, UPDATE_READY,
                      NO_ACTION, NEW_UPDATE):
        return json.dumps({"status":returncode, "package_list":[]})
    
    for package_entry in update_info.split("\n"):
        package_name=parse_package_name(package_entry)
        if package_name == None:
            continue
        description=parse_package_description(package_entry)
        packages.append({"package_name": package_name, "description":description})

    return json.dumps({"status":returncode, "package_list": packages})


def get_status():
    if (getAptBusy( )):
        return json.dumps({"status": "busy"})

    return json.dumps({"status": "free"})


def update(self):
    command = "sudo pi-update -a"
    err = os.system(command)

    return err


def perform_update(self):
    err = update()
    
    if err == DPKG_CONFIG_NEEDED:
        return json.dumps({"status": DPKG_CONFIG_NEEDED})
    else:
        return json.dumps({"status": "success"})


def error():
    return json.dumps("Error")


def op_dispatch(form):
    # Do a dispatch on the operation
    op = form.getfirst("op")
    args = dict((k, form[k].value) for k in form.keys() if not k=="op")

    op_dict = {
        "get_status"   : get_status,
        "update"       : update,
        "get_packages" : get_packages
    }

    op_func = op_dict.get(op, error)
    composeJS(op_func())

    
def main():
    form = cgi.FieldStorage()
    try:
	op_dispatch(form)
    except:
    	composeJS(error())
        
if __name__ == "__main__":
    main()
            
