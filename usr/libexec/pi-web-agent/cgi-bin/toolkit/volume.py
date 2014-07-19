#!/usr/bin/python
import json
import os, sys
from live_info import execute
import cgi, cgitb
cgitb.enable()
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME'] + '/etc/config')

from HTMLPageGenerator import composeJS
from framework import view, output
import re

def get_volume():
    # Returns current volume of Master    
    out, exit_code = execute("sudo amixer sget Master")
    m = re.search("[0-9]+%", out)
    vol = m.group(0)[:-1]
    
    return int(vol)

def set_volume(n_vol):
    command = "sudo amixer sset Master {vol}\%"
    out, exit_code = execute(command.format(vol=n_vol))

    return n_vol

def main():
    # main entry point for the volume controller api
    # do a dispatch on the url command and call
    # the corresponding function
    #
    # If no value is given returns current volume
    # otherwise sets volume to the update value in
    # the form from GET
    #
    # Need to also check for not well formed URLs
    form = cgi.FieldStorage()

    try:
        new_vol = form['update'].value
        n_vol = set_volume(int(new_vol))
        composeJS(json.dumps(n_vol))
    except KeyError:
        current_vol = get_volume()
        composeJS(json.dumps(current_vol))

if __name__ == "__main__":
    main()





