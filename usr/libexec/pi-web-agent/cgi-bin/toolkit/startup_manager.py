#!/usr/bin/python
import sys, cgi, os
import cgitb
cgitb.enable()
EXTENSION_ID='Startup Manager'
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME'] + '/cgi-bin/toolkit')
sys.path.append(os.environ['MY_HOME'] + '/cgi-bin/chrome')
sys.path.append(os.environ['MY_HOME'] + '/objects')
sys.path.append(os.environ['MY_HOME'] + '/scripts')
sys.path.append(os.environ['MY_HOME'] + '/etc/config')

from framework import output, view, config, get_template
import json

CONFIG_FILE = '/usr/share/pi-web-agent/startup/startup.cfg'

class StartupManager(object):
    
    def getView(self):
        tFile = open(get_template('startup_controller'))
        html = tFile.read()
        tFile.close()
        return html
        
    def getStartupDefinitions(self):
        jFile = open(CONFIG_FILE)
        definition = json.load(jFile)
        jFile.close()
        return definition
        
    def setStartupDefinition(self, script_location, args, executeNow=False):
        jFile = open(CONFIG_FILE)
        definition = json.load(jFile)
        jFile.close()
        definition.append({'script':script_location, 'args':args})
        jFile = open(CONFIG_FILE, 'w')
        json.dump(definition, jFile)
        exitcode = 0
        if (executeNow):
            result, exitcode = execute(script_location + ' ' + args)
        return {'code':exitcode}
        
def main():
    form = cgi.FieldStorage()
    startupMgr = StartupManager()
    view.setContent('Startup Manager', startupMgr.getView())
    output(view, form)
    
if __name__ == "__main__":
    main()
