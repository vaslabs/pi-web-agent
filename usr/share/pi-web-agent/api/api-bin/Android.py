import os
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
API_PATH='/usr/share/pi-web-agent/api'
import xml.etree.ElementTree as ET
class Android(object):
    
    def __init__(self):
        self.response=self.generateDefaultResponse() #ET
    
    def toAndroidXML(self):
        raise NotImplementedError
        
    def generateDefaultResponse(self):
        el_response=ET.Element('response',{'version':'0.1'})
        el_widgets=ET.Element('widgets')
        el_submit=ET.Element('submit')
        
        el_url=ET.Element('url')
        
        el_format=ET.Element('format')
        el_furl=ET.Element('url')        
        
        el_format.append(el_furl)
        
        el_submit.append(el_url)
        el_submit.append(el_format)
        
        el_response.append(el_widgets)
        el_response.append(el_submit)
        return el_response
import os
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
API_PATH='/usr/share/pi-web-agent/api'
import xml.etree.ElementTree as ET
class Android(object):
    
    def __init__(self):
        self.response=self.generateDefaultResponse() #ET
    
    def toAndroidXML(self):
        raise NotImplementedError
        
    def generateDefaultResponse(self):
        el_response=ET.Element('response',{'version':'0.1'})
        el_widgets=ET.Element('widgets')
        el_submit=ET.Element('submit')
        
        el_url=ET.Element('url')
        
        el_format=ET.Element('format')
        el_furl=ET.Element('url')        
        
        el_format.append(el_furl)
        
        el_submit.append(el_url)
        el_submit.append(el_format)
        
        el_response.append(el_widgets)
        el_response.append(el_submit)
        return el_response

