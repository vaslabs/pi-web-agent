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
#required for working with http status codes
import httplib

config=Configuration()
view = View(config.system.actions, config.system.cmdactions)

def get_template(template):
    return gt(template)

def output(view, form):
    if "type" in form and form["type"].value == "js":
        view.js_output()
    else:
        view.output()


        
#replaces deprecated html page generator function
#(the mplayer version is used since code gets a 
#default value)
#USED TO SET APPLICATION/JSON(content-type)HEADER 
#AND APPROPRIATE HTTP STATUS CODE
#\---> FOR PRINTING JSON REPLIES
def composeJS(stringifiedJSON, code=httplib.OK):
    print 'Status: ', code, ' ', httplib.responses[code]
    print 'Content-Type: application/json'
    print 'Cache-Control: no-store'
    print 'Length:', len(stringifiedJSON)
    print ''
    print stringifiedJSON
    
#from html page generator/ used in chrome/view.py
#USED TO SET TEXT/HTML(contnet-type) HEADER
#\---> FOR PRINTING HTML REPLIES
def outputHTMLDocument(*parts):
    print "Content-type: text/html"
    print
    print '<!DOCTYPE html>'
    for part in parts:
        print part
        
#from html page generator
#used in camera_utils.py installUninstallPackage.py
#USED TO SET TEXT/HTML(contnet-type) HEADER
#\---> FOR PRINTING XML REPLIES
def composeXMLDocument(xml):
    print "Content-type: text/html"
    print
    print ET.tostring(xml, encoding='UTF-8')

def requestDefinition(extensionID):
    return config.system.actions[extensionID]
        
def getDependencies(extensionID):
    return config.system.actions[extensionID]['dependencies']
