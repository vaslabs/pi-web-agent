#!/usr/bin/python
import sys
import os
import xml.etree.ElementTree as ET
from random import random, seed
import ast
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/toolkit')
sys.path.append(os.environ['MY_HOME']+'/etc/config')
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/chrome')
sys.path.append(os.environ['MY_HOME']+'/cgi-bin')

from cern_vm import Configuration
from view import View
import cgi
import cgitb
from HTMLPageGenerator import *
import cern_vm
cgitb.enable()

class InvalidXMLException(Exception):
    AUTH_ERROR=30
    BAD_TAG=22
    API_DISABLED=10
    CALLED_FROM_BROWSER = 401 
    def __init__(self, message=None, code=None):
        Exception.__init__(self)
        if message == None:
            self.strerror=""
        else:
            self.strerror=message
        
        if code == None or (code < 0 or code > 500):
            self.ex_code=500
        else:
            self.ex_code = code
        
    def __str__(self):
        return "InvalidXMLException: " + self.strerror + "\nCode:" + str(self.ex_code)

        
class RequestManager(object):

    def __init__(self, xml):
        self.xml=xml
        self.check_validity()
        self.username=findSingleElement('username', self.xml).text
        self.apikey=findSingleElement('apikey', self.xml).text
        self._authenticate()
        self.id = str(random()).split('.')[1] 
        requestElement=findSingleElement('add', self.xml)
        if requestElement == None:
            requestElement=findSingleElement('remove', self.xml)
            if requestElement != None:
                self.request = RemoveRequest(requestElement, self.id)
                return
            requestElement = findSingleElement('list', self.xml)
            if requestElement == None:
                raise InvalidXMLException(message='Missing request tag <add> or <remove>')
            self.request = ListRequest(requestElement, self.id)
        else:    
            self.request = AddRequest(requestElement, self.id)
       
    def _authenticate(self):
        data=None
        try:
            with open(os.environ['MY_HOME']+"/etc/config/.api_access", "r") as regFile:
                data = ast.literal_eval(regFile.readline())
        except IOError as ioe:
            raise InvalidXMLException('API not enabled', InvalidXMLException.API_DISABLED)
            
        username = data.keys()[0]
        apikey = data[username]
        if username == self.username and apikey == self.apikey:
            return
        else:
            raise InvalidXMLException('Authentication failure', InvalidXMLException.AUTH_ERROR)
            

    def submit(self):
        self.request.doTransaction()

    def check_validity(self):
        if self.xml.tag != HEADER:
            raise InvalidXMLException(message="Uknown tag: " + self.xml.tag, code=InvalidXMLException.BAD_TAG)

        
def findSingleElement(key, xml):
        element=xml.findall(key)
        if len(element) > 1:
            raise InvalidXMLException(message='Multiple tag: ' + key)
        if len(element) == 0:
            return None    
        return element[0]        

HEADER="cernvm-api"
SUPPORTED_VERSIONS=["1.0"]

#abstract class Request / Pattern: Template for other requests
class Request(object):
    
     
    
    def __init__(self, request, rmID):
        self.xml=request
        seed(os.urandom)
        self.req_id=rmID

    def doTransaction(self):
        try:        
            self._parse()  
            self._validate()
            self._construct()
            self._execute()
            self._response()
            self._register()
        except InvalidXMLException as ixe:
            self._response(ixe)
            
    def _parse(self):
        raise NotImplementedError()
        
    def _execute(self):
        
        raise NotImplementedError()
    
    def _validate(self):
        raise NotImplementedError()

    def _construct(self): 
        raise NotImplementedError()

    def _register(self):
        with open(os.environ['MY_HOME']+"/etc/config/register", "a") as regFile:
            regFile.write(str(self.req_id)+':'+str(self.code))
    
            
    def _response(self, ex=None):
        response = Response(self.req_id)
        if ex==None:
            responseCode = 0
        else:
            responseCode = ex.ex_code
        self.code = responseCode
        response.buildResponse(responseCode)
        composeXMLDocument(response.xml)

                
class AddRequest(Request):

    def _parse(self):
        self.title=findSingleElement('title', self.xml).text
        if self.title == None:
            raise InvalidXMLException(message='Tag <title> not found')    
        self.id=findSingleElement('id', self.xml)
        if (self.id == None):
            self.id = self.title
        self.commandgroups=self.xml.findall('command-group')
        if len(self.commandgroups) == 0:
            raise InvalidXMLException(message='Tag <add> without tag <command-group>')
        self.cg_map={}
        cgID=1
        for command_group in self.commandgroups:
            commands=command_group.findall('command')
            if len(commands) == 0:
                raise InvalidXMLException(message='Tag <command-group> has no <command> tags')
            self.cg_map['1']=commands
    
            
    def _validate(self):
        configuration = Configuration()
        if self.id in configuration.system.actions:
            raise InvalidXMLException(message='Action with id ' + self.id + ' already exists!')
    
        
    def _construct(self):
        action_el = ET.Element('action')
        
        title_el = ET.Element('title')
        title_el.text = self.title
        
        id_el = ET.Element('id')
        id_el.text=self.id
        
        url_el = ET.Element('url')
        url_el.text = '/cgi-bin/toolkit/main.py?page=' + self.id
        
        action_el.append(title_el)
        action_el.append(id_el)
        action_el.append(url_el)
        
        for cg in self.cg_map:
            cg_el=ET.Element('command-group', {'id':cg})
            for command in self.cg_map[cg]:
                cg_el.append(command)
            action_el.append(cg_el)
        self.action = action_el     
                
    def _execute(self):
        xml=ET.parse(cern_vm.CONFIG_PATH + '/.actions')
        xml_file=xml.getroot()
        xml_file.append(self.action)
        xml._setroot(xml_file)
        xml.write(cern_vm.CONFIG_PATH + '/.actions')
        #uncomment the above when testing is done
        #and comment the below
        self.xml_file = xml_file        
    
    
            
class RemoveRequest(Request):
    
    def _parse(self):
        self.id = findSingleElement('id', self.xml).text
        if self.id == None:
            raise InvalidXMLException('id tag missing')
            
    def _construct(self):
        xml=ET.parse(cern_vm.CONFIG_PATH + '/.actions')
        el_actions = xml.getroot().findall('action')
        for action in el_actions:
            el_id = action.find('id')
            if self.id in el_id.text:
                xml.getroot().remove(action)
                self.xml_file = xml
                return
        raise InvalidXMLException(message='Action with id ')      
    
    def _execute(self):
        self.xml_file.write(cern_vm.CONFIG_PATH + '/.actions')
        
    def _validate(self):
        self.configuration = Configuration()
        if self.id not in self.configuration.system.actions.keys():
            raise InvalidXMLException(message='Action with id ' + self.id + ' does not exist!')

class ListRequest(Request):
    
    def _parse(self):
        pass
    
    def _construct(self):
        xml=ET.parse(cern_vm.CONFIG_PATH + '/.actions')
        el_actions = xml.getroot().findall('action')
        self.response_xml = ET.Element('list')
        for action in el_actions:
            el_id = action.find('id')
            el_action = ET.Element('action', {'id':el_id.text})
            self.response_xml.append(el_action)
        
    def _response(self, ex=None):
        response = Response(self.req_id)
        if ex==None:
            responseCode = 0
            self.code = responseCode
            response.buildResponse(responseCode)
            response.xml.append(self.response_xml)
            composeXMLDocument(response.xml)
            return
        
        responseCode = ex.ex_code
        self.code = responseCode
        response.buildResponse(responseCode)
        composeXMLDocument(response.xml)     
        
        
    def _execute(self):
        pass
        
    def _validate(self):
        pass
                
class Response(object):    

    def __init__(self, rID):

        self.id=rID
        pass
    
    def buildResponse(self, rcode, message=None):
        req=ET.Element('request')
        req.text=str(self.id)
        code=ET.Element('code')
        if message == None:
            code.text=str(rcode)
        else:
            code.text = str(rcode) + ' ' + message
        self.xml=ET.Element('cernvm-api', {'version':'1.0'})
        self.xml.append(req)
        self.xml.append(code)                

def main():
    fs=cgi.FieldStorage()
    if 'xml' not in fs:
        ixe = InvalidXMLException('not a post maybe called from browser',\
         InvalidXMLException.CALLED_FROM_BROWSER)
        
    transaction=ET.fromstring(fs['xml'].value)
    try:
        rm=RequestManager(transaction)
        rm.submit()
    except InvalidXMLException as ixe:
        response=Response(0)
        response.buildResponse(ixe.ex_code)
        composeXMLDocument(response.xml)


if __name__ == '__main__':
    try:
        main()
    except InvalidXMLException as ixe:
        r=Response(0)
        r.buildResponse(ixe.code)     
        composeXMLDocument(r.xml)
