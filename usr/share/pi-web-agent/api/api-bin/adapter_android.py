#!/usr/bin/python
import os, sys#, cgi
#import cgitb
#cgitb.enable()
from Android import Android
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/toolkit')
sys.path.append(os.environ['MY_HOME']+'/etc/config')
from Adapter import GenericAdapter
from framework import config, view
import xml.etree.ElementTree as ET

class AdapterAndroid(GenericAdapter, Android):

    def __init__(self, title, view, commandgroup):
        GenericAdapter.__init__(self, title, view, commandgroup)
        Android.__init__(self)

    def page(self):
        el_listview_adapter=ET.Element('widget', {'type':'listview'})
        for commandIDs in self.commandgroup:
            elements=self._message(self.commandgroup[commandIDs])
            #element_type=self._message(command.format)
            el_subpage_adapter=self._subpage(elements)
            el_listview_adapter.append(el_subpage_adapter)

        widgets=self.response.findall('widgets')[0]
        widgets.append(el_listview_adapter)
        viewTree = ET.ElementTree()
        viewTree._setroot(self.response)
        return viewTree

    def _subpage(self, elements, title=None):
        html=''
        for element in elements:
            html+=element+': ' + elements[element] + '\n'
        if elements[element].format=='table':
            el_subpage_adapter=ET.Element('widget', {'type':'table'})
        else:
            el_subpage_adapter=ET.Element('widget', {'type':'textview'})
        el_subpage_adapter.text=html
        return el_subpage_adapter

    def toAndroidXML(self):
        return ET.tostring(self.page().getroot(), encoding='utf8')

def main():
    #fs=cgi.FieldStorage()
    fs={'page':'System Information'}    
    ID=fs['page']
    try:
        action=config.system.actions[ID]
    except KeyError as ke:
        view.setContent('Page not found', 'The requested page was not found. Did you type the url manually?')
        view.output()
        return
    ada=AdapterAndroid(ID,view,action.command_groups)
    print ada.toAndroidXML()

main()
