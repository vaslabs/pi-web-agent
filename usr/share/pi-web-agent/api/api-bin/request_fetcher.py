#!/usr/bin/python
import sys, os
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME']+'/cgi-bin')
import cgi, cgitb
from random import random, seed
cgitb.enable()
from HTMLPageGenerator import *
from pi_api import SimpleAuthenticationRequest, InvalidXMLException, Response
FORMAT_PATH="/usr/share/pi-web-agent/api"
def main():
    form = cgi.FieldStorage()
    if 'xml' not in form:
        ixe = InvalidXMLException('Post might be called from browser',\
         InvalidXMLException.CALLED_FROM_BROWSER)
        raise ixe
    request_xml = ET.fromstring(form['xml'].value)
    el_authentication_list = request_xml.findall('authentication')
    if len(el_authentication_list) == 0:
        raise InvalidXMLException('Post might be called from browser',\
         InvalidXMLException.AUTH_ERROR)
    el_authentication = el_authentication_list[0]       
    sar = SimpleAuthenticationRequest(el_authentication, str(random()).split('.')[1])
    sar.doTransaction()  
    el_format = request_xml.find('format')
    if (el_format == None):
        raise InvalidXMLException('Bad tag', InvalidXMLException.BAD_TAG)

    xml = ET.parse(FORMAT_PATH + el_format.text)
    composeXMLDocument(xml.getroot())
    
if __name__ == '__main__':
    try:
        main()    
    except InvalidXMLException as ixe:
        r=Response(0)
        r.buildResponse(ixe.ex_code)     
        composeXMLDocument(r.xml)
