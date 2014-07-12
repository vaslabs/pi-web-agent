#!/usr/bin/python
import sys
import os
import string
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME'] + '/cgi-bin/toolkit')
sys.path.append(os.environ['MY_HOME'] + '/cgi-bin/chrome')
sys.path.append(os.environ['MY_HOME'] + '/objects')
sys.path.append(os.environ['MY_HOME'] + '/scripts')
sys.path.append(os.environ['MY_HOME'] + '/etc/config')


from live_info import execute
import cgi
import cgitb
from subprocess import Popen, PIPE
cgitb.enable()
from framework import output, view, config
from DependableExtension import DependableExtension

EXTENSION_ID='Pi Camera Controller'

class CameraManager(DependableExtension):

    def __init__(self):
        DependableExtension.__init__(self, EXTENSION_ID)
        
    def getNormalView(self):
        pictures, returncode = execute("ls /usr/share/pi-web-agent/camera-media/*.jpg")
        linearray = pictures.split('\n')
    
        html = '''<div id="camera_toolbar">
                  <div class="btn-group btn-group-justified">
                      <a href='javascript:navigate("/cgi-bin/toolkit/camera.py?type=js")' class="btn btn-default">Live stream</a>
                      <a href='javascript:camera_utils("snapshot")' class="btn btn-default">Snapshot</a>
                      <a href='javascript:alert("Coming soon")' class="btn btn-default">Record</a>
                      <a href='javascript:camera_utils("stoprecord")' class="btn btn-default">Stop</a>
      
                 </div></div><br>
          '''
        html += '''<div id="gallery_thumbnails">'''
    
        for thisline in linearray:
            justname = thisline.split('/')[-1]
            if len(justname) <= 0:
                continue
            html += '<a href="/cgi-bin/toolkit/image_manager.py?image='+justname +'" rel="thumbnail"><img style="padding:4px; border:2px solid #021a40;" src="/cgi-bin/toolkit/image_manager.py?image='+justname.split('.')[0]+'.png" style="width: 64px; height: 64px" /></a>'
        
        html += '</div><br>'
        return html
    
    def generateView(self):
        if (not self.check_status()):
            return self._generateMissingDependenciesView()
        return self.getNormalView()

def main():

    form = cgi.FieldStorage()
    
    cameraMgr = CameraManager()
    view.setContent('Pi Camera Controller', cameraMgr.generateView())
    output(view, cgi.FieldStorage())
    
if __name__ == '__main__':
    main()
