#!/usr/bin/python
import os, sys, cgi
from Android import Android
from random import random, seed
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/toolkit')
sys.path.append(os.environ['MY_HOME']+'/cgi-bin')
from HTMLPageGenerator import composeXMLDocument
from power_management import PowerManager
import power_management
import xml.etree.ElementTree as ET
from pi_api import SimpleAuthenticationRequest, InvalidXMLException, Response

class PowerManagementAndroid(PowerManager, Android):

    def __init__(self):
        PowerManager.__init__(self)
        Android.__init__(self)

    def getSuccessView(self, message):
        el_textview_powerlist=ET.Element('widget', {'type':'textview'})

        el_respond_powerlist=ET.Element('respond')
        el_respond_powerlist.text=message
        el_textview_powerlist.append(el_respond_powerlist)

        el_uri_powerlist=ET.Element('uri')
        el_uri_powerlist.text='powma://respond_message'
        el_textview_powerlist.append(el_uri_powerlist)

        widgets=self.response.findall('widgets')[0]
        widgets.append(el_textview_powerlist)
        viewTree = ET.ElementTree()
        viewTree._setroot(self.response)
        return viewTree

    def getDefaultView(self):
        el_droplist_powerlist=ET.Element('widget', {'type':'droplist'})

        el_entries_powerlist=ET.Element('entries')
        el_droplist_powerlist.append(el_entries_powerlist)

        el_entry_shutdown=ET.Element('entry')
        el_entry_shutdown.text='Shut down'
        el_entries_powerlist.append(el_entry_shutdown)

        el_entry_restart=ET.Element('entry')
        el_entry_restart.text='Restart'
        el_entries_powerlist.append(el_entry_restart)

        el_label_powerlist=ET.Element('label')
        el_label_powerlist.text='Power Options'
        el_droplist_powerlist.append(el_label_powerlist)

        el_uri_powerlist=ET.Element('uri')
        el_uri_powerlist.text='powma://power_list'
        el_droplist_powerlist.append(el_uri_powerlist)

        el_submit = self.response.findall('submit')[0]        
        el_url=el_submit.findall('url')[0]
        el_url.text='/api-bin/power_management_android.py'

        el_format=el_submit.findall('format')[0]
        el_format_url=el_format.findall('url')[0]
        el_format_url.text='/xml/formats/power_management_request.xml'

        widgets=self.response.findall('widgets')[0]
        widgets.append(el_droplist_powerlist)
        viewTree = ET.ElementTree()
        viewTree._setroot(self.response)
        return viewTree



       

def main():
    powma=PowerManagementAndroid()
    powm=PowerManager()
    form=cgi.FieldStorage()
    if 'xml' not in form:
        raise InvalidXMLException('No xml request', InvalidXMLException.CALLED_FROM_BROWSER)
    req=ET.fromstring(form['xml'].value)
    el_authentication_list = req.findall('authentication')
    if len(el_authentication_list) == 0:
        raise InvalidXMLException('Post might be called from browser',\
         InvalidXMLException.AUTH_ERROR)
    el_authentication = el_authentication_list[0]
    sas = SimpleAuthenticationRequest(el_authentication,str(random()).split('.')[1])
    sas.doTransaction()
    el_pair = req.findall('pair')[0]
    req_key=el_pair.find('key')
    req_value=el_pair.find('value')
    if (req_key.text=='def://power_management'):
        if (req_value.text=='default'):
            response = powma.getDefaultView()
        else:
            raise Exception
    elif (req_key.text=='powma://power_list'):
        if (req_value.text=='Restart'):
            response = powma.getSuccessView('Restarting')
            powm.execute_command(power_management.RESTART)
        elif (req_value.text=='Shut down'):
            response = powma.getSuccessView('Shutting down')
            powm.execute_command(power_management.POWEROFF)
        else:
            raise Exception
    else:
        raise Exception
    
    composeXMLDocument(response.getroot())
#testing
if __name__ == '__main__':
    try:
        main()        
    except InvalidXMLException as ixe:
        r=Response(0)
        r.buildResponse(ixe.ex_code)     
        composeXMLDocument(r.xml)


