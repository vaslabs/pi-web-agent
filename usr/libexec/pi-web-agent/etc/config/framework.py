import sys
import os
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME']+'/etc/config')
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/chrome')
from cern_vm import Configuration
from view import View

config=Configuration()
view = View(config.system.actions)

def output(view, form):
    if "type" in form and form["type"].value == "js":
        view.js_output()
    else:
        view.output()

