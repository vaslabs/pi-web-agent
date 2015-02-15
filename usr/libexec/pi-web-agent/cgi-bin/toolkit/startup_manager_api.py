#!/usr/bin/python
from startup_manager import StartupManager
startupMgr = StartupManager()
import json
import cgi
from view import composeJS

def get_current_definitions():
    return startupMgr.getStartupDefinitions()
    

def set_definition(script, arguments, executeNow=False):
    return startupMgr.setStartupDefinition(script, arguments, executeNow)
    

def valid(form):
    return 'script' in form
    
def remove_definition(index):
    return startupMgr.remove_definition(index)

def main(form):
    
    if 'cmd' in form:
        if form['cmd'].value == 'set':
            if (valid(form)):
                script = form['script'].value
                arguments = ""
                if 'args' in form:
                    arguments = form['args'].value
                result = set_definition(script, arguments)
                composeJS(json.dumps(result))
            else:
                composeJS(json.dumps({'status':'INVALID_DATA'}))
        elif form['cmd'].value == 'get':
            result = get_current_definitions()
            composeJS(json.dumps(result))
        elif form['cmd'].value == 'remove' and 'index' in form:
            index = int(form['index'].value)
            result = remove_definition(index)
            composeJS(json.dumps(result))
    else:
        composeJS(json.dumps({'status':'INVALID_DATA'}))
        
if __name__ == "__main__":
    main(cgi.FieldStorage())
