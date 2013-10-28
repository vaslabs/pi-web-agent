#!/usr/bin/python
import cgi
import cgitb
import os
cgitb.enable()
import sys
sys.path.append(os.environ['MY_HOME']+'/scripts')
sys.path.append(os.environ['MY_HOME']+'/etc/config')
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/chrome')
sys.path.append(os.environ['MY_HOME']+'/cgi-bin')
from cern_vm import Configuration
from view import View
from HTMLPageGenerator import *
from BlueprintDesigner import *
import random
import crypt
import ast
class APIManager(object):

    def __init__(self):
        try:
            self.readCurrentApi()
        except:
            self.data=None
            
    def getDefaultView(self):
        if self.data == None:
            secondary_text=''
            iw_checkbox=InputWidget('checkbox', 'api_enable_disable',\
            '', ' Enable API')
        else:
            iw_checkbox=InputWidget('checkbox', 'api_enable_disable',\
            '', 'Enable API', attribs='checked')
            secondary_text='Username: ' + self.data.keys()[0] + '<br>'
            secondary_text+='apikey: ' + self.data[self.data.keys()[0]]
        iw_submit=InputWidget('submit', '', 'submit', '',wClass='btn btn-primary')
        iwg = InputWidgetGroup()
        iwg.widgets=[iw_checkbox, iw_submit]
        
        if len(secondary_text) == 0:
            return fieldset('/cgi-bin/toolkit/enable_api.py', 'POST',\
            'api_form', iwg, createLegend("API Management"))
        else:
            return '<div>' + secondary_text + '<br>' + \
            fieldset('/cgi-bin/toolkit/enable_api.py', 'POST',\
            'api_form', iwg, createLegend("API Management")) +\
            '</div>'
            
    def getAppliedView(self):
        msg="username: admin<br><br>"
        msg+="apikey: " + self.apikey
        return createLegend(msg)         

    def generateApiKey(self):
        self.apikey=crypt.crypt(str(random.random()), str(random.random()).split('.')[1])
        with open(os.environ['MY_HOME']+"/etc/config/.api_access", "w") as regFile:
            regFile.write('{\'admin\':'+'\''+str(self.apikey)+'\'}')

    def disableApi(self):
        os.remove(os.environ['MY_HOME']+"/etc/config/.api_access")
        
    def getDisabledView(self):
        message="API is disabled!"
        return createDiv(message, 'error')    
    
    def readCurrentApi(self):
        with open(os.environ['MY_HOME']+"/etc/config/.api_access", "r") as regFile:
            self.data = ast.literal_eval(regFile.readline())
                    
def main():
    form = cgi.FieldStorage()
    config=Configuration()
    view = View(config.system.actions)
    apiMgr = APIManager()
    if 'content-length' not in form.headers:
        view.setContent('API management', apiMgr.getDefaultView())
        view.output()
        
    else:
        if form.getvalue('api_enable_disable'):
            apiMgr.generateApiKey()
            view.setContent("API management", apiMgr.getAppliedView())
            view.output()
        else:
            try:
                apiMgr.disableApi()
            except IOError:
                pass
            view.setContent("API management", apiMgr.getDisabledView())
            view.output()
if __name__ == '__main__':
    main()
