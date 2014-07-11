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

    if not m:
        return "Couldn't get volume!"

    return m.group(0)





