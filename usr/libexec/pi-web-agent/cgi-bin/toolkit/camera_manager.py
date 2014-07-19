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
from framework import output, view, config, get_template
from DependableExtension import DependableExtension
import json

EXTENSION_ID='Pi Camera Controller'

class CameraManager(DependableExtension):

    def __init__(self):
        DependableExtension.__init__(self, EXTENSION_ID)
        
    def getImages(self):
        
        pictures, returncode = execute("ls /usr/share/pi-web-agent/camera-media/*.png")
        if (returncode != 0):
            linearray = [returncode]
        else:
            linearray = pictures.split('\n')
            for i, value in enumerate(linearray):
                linearray[i] = os.path.basename(value)
            del linearray[-1]
        return linearray
        
    def getNormalView(self):
        tFile = open(get_template('camera_controller'))
        html = tFile.read()
        tFile.close()

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
