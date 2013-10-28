#!/usr/bin/python
import os, sys
from Android import Android
if 'MY_HOME' not in os.environ:
	os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/toolkit/')
from update import UpdateManager
import xml.etree.ElementTree as ET
import cgi

class UpdateManagerAndroid(UpdateManager, Android):
	
	def __init__(self):
		UpdateManager.__init__(self)
		Android.__init__(self) #initialises self.response

	def getUpdatesAvailableView(self):
		el_widgets = self.response.findall('widgets')[0]		
		el_title=ET.Element('widget', {'type':'textview', 'heading':'2'})
		el_title.text='Updates are available!'
		el_widgets.append(el_title)

		el_submit = self.response.findall('submit')[0]		
		el_url=el_submit.findall('url')[0]
		el_url.text='/api-bin/update_android.py'

		el_format=el_submit.findall('format')[0]
		el_format_url=el_format.findall('url')[0]
		el_format_url.text='/xml/formats/update_request.xml'

		viewTree = ET.ElementTree()
		viewTree._setroot(self.response)
		return viewTree
	
	def getNoUpdatesAvailableView(self):
		el_widgets = self.response.findall('widgets')[0]		
		el_title=ET.Element('widget', {'type':'textview', 'heading':'2'})
		el_title.text='System is up to date!'
		el_widgets.append(el_title)
	
		viewTree = ET.ElementTree()
		viewTree._setroot(self.response)
		return viewTree

	def toAndroidXML(self):
		xml_view=self.getNoUpdatesAvailableView()
		return ET.tostring(xml_view.getroot(), encoding='utf8')

uma = UpdateManagerAndroid()



print uma.toAndroidXML()

