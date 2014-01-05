#!/usr/bin/python
import xml.etree.ElementTree as ET
import os

CONFIG_FILE=os.environ['MY_HOME']+"/etc/config/config.xml"
CONFIG_PATH=os.environ['MY_HOME']+"/etc/config"
VERSION="0.1-rc-3"
def parseActions(actionTree, secondary=False):
        actions={}
        
        for xmlaction in actionTree:
            attribs={'title':'','id':'','url':'', 'command-group':{}}
            for attribute in xmlaction:
                if attribute.tag != 'command-group':
                    attribs[attribute.tag]=attribute.text
                else:
                    cgID=attribute.attrib['id']
                    cgTag=attribute.tag
                    attribs[cgTag][cgID]=[]
                    for command in attribute:
                        commandTitle=command.attrib['title']
                        try:
                            commandFormat=command.attrib['format']
                        except:
                            commandFormat=None
                        value=command.text
                        cmd=Command(commandTitle, commandFormat, value)
                        attribs[cgTag][cgID].append(cmd)
                        
            aID=attribs['id']
            aTitle=attribs['title']
            aURL=attribs['url']
            aCmg=attribs['command-group']
            actions[aID]=Action(aTitle, aID, aURL, aCmg, secondary)
            
        return actions
        
class Configuration(object):
    
    def __init__(self):
        self.configTree=ET.parse(CONFIG_FILE)
        root=self.configTree.getroot()   
       
        #assume version 1.0 for now
        if root[0].tag != 'system':
            raise Exception('Invalid Configuration File')
        systemTree=root[0]    
        self.system=System()
        extActions=[]
        try:
            self.extensionFile=root[0].attrib['extension']
            extRoot=ET.parse(CONFIG_PATH+'/'+self.extensionFile).getroot()
            actionTree=extRoot
            extActions=parseActions(actionTree, True)
        except:
            pass
        
        actions=parseActions(systemTree)
            
        self.system.addActions(actions)
        self.system.addActions(extActions)

class System(object):
    
    def __init__(self):
        self.actions={}
        
    def addAction(self, action):
        self.actions.append(action)
    
    def addActions(self, actions):
        for action in actions:
            self.actions[action]=actions[action]

 
class Action(object):
            
    
    def __init__(self, title, aID, url, command_groups, secondary=False):
        self.title=title
        self.id=aID
        self.url=url
        self.command_groups=command_groups
        self.secondary=secondary
        self.format = None
        
    
    def setFormat(self, format):
        self.format = format
    
    
    def toXML(self):
        el_main=ET.Element('action')
        el_title=ET.Element('title')
        el_title.text = self.title
        el_id = ET.Element('id')
        el_id.text = self.id
        el_url = ET.Element('url')
        el_url.text = self.url
        el_main.append(el_title)
        el_main.append(el_id)
        el_main.append(el_url)
        
        for cg in self.command_groups:
            el_command_group = ET.Element('command-group')
            for command in self.command_groups[cg]:
                el_command=command.toXML()
                el_command_group.append(el_command)
            el_main.append(el_command_group)
        
        return el_main        
        
        
class Command(object):
    
    def __init__(self, title, format, value):
        self.title=title
        self.format=format
        self.value=value
    
    def toXML(self):
        el_command=ET.Element('command-group', {'title':self.title})
        if not self.format == None and not len(self.format) == 0:
            el_command.set('format', self.format)
        el_command.text = self.value        
        return el_command
            

