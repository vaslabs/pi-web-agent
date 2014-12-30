import sys
import os
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME']+'/etc/config')
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/chrome')
sys.path.append(os.environ['MY_HOME']+'/objects')
from pi_web_agent import Configuration
from view import get_template as gt
from view import View

config=Configuration()
view = View(config.system.actions, config.system.cmdactions)

def get_template(template):
    return gt(template)

def output(view, form):
    if "type" in form and form["type"].value == "js":
        view.js_output()
    else:
        view.output()
        
def requestDefinition(extensionID):
    return config.system.actions[extensionID]
        
def getDependencies(extensionID):
    return config.system.actions[extensionID]['dependencies']
