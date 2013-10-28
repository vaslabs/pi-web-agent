#!/usr/bin/python
import os, sys
from Android import Android
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME']+'/scripts')
from PasswordManager import PasswordManager
import xml.etree.ElementTree as ET

class PasswordManagerAndroid(PasswordManager, Android):

    def __init__(self, form, username='admin'):
        PasswordManager.__init__(self, form, username)
        Android.__init__(self)
        
    def getDefaultView(self):
        el_inputboxcurr=ET.Element('widget', {'type':'inputbox'})
        el_labelcurr=ET.Element('label')
        el_labelcurr.text='New password'
        el_uricurr=ET.Element('uri')
        el_uricurr.text='pm://current'
        el_inputboxcurr.append(el_labelcurr)	
        el_inputboxcurr.append(el_uricurr)

        el_inputboxnew1=ET.Element('widget', {'type':'inputbox'})
        el_labelnew1=ET.Element('label')
        el_labelnew1.text='New password'
        el_urinew1 = ET.Element('uri')
        el_urinew1.text='pm://new1'	
        el_inputboxnew1.append(el_labelnew1)
        el_inputboxnew1.append(el_urinew1)

        el_inputboxnew2=ET.Element('widget', {'type':'inputbox'})
        el_labelnew2=ET.Element('label')
        el_labelnew2.text='Retype password'
        el_urinew2 = ET.Element('uri')
        el_urinew2.text='pm://new2'       

        el_inputboxnew2.append(el_labelnew2)
        el_inputboxnew2.append(el_urinew2)

        widgets=self.response.findall('widgets')[0]
        widgets.append(el_inputboxcurr)
        widgets.append(el_inputboxnew1)
        widgets.append(el_inputboxnew2)
        viewTree = ET.ElementTree()
        viewTree._setroot(self.response)
        return viewTree
        
    def toAndroidXML(self):
        xml_view=self.getDefaultView()
        return ET.tostring(xml_view.getroot(), encoding='utf8')
        
        
#just for testing
'''
self.password=self.form.getvalue("passwd")
        self.password1=self.form.getvalue("passwd_new1")
        self.password2=self.form.getvalue("passwd_new2")
'''
form={'passwd':123, 'passwd_new1':1234, 'passwd_new2':1234}
pma = PasswordManagerAndroid(form)
print pma.toAndroidXML()

