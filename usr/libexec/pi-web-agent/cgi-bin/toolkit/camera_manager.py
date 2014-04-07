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

from live_info import execute
from services import *
from view import *
from cern_vm import Configuration
import cgi
import cgitb
from subprocess import Popen, PIPE
cgitb.enable()
from framework import output

def main():

    form = cgi.FieldStorage()
    sm=serviceManagerBuilder()
    config=Configuration()
    view = View(config.system.actions)
    
    pictures, returncode = execute(os.environ['MY_HOME'] + "/scripts/get_pictures.sh /usr/libexec/pi-web-agent/cgi-bin/toolkit")
    linearray = pictures.split('\n')
    
    html = '<div id="camera_toolbar">'
    html += '<a id="makePreview" class="btn btn-primary" onclick="camera_utils("play")">Play</a>'
    html += '<a id="takeSnapshot" class="btn btn-primary" onclick="camera_utils("snapshot")">Snapshot</a>'
    html += '<a id="startRecord" class="btn btn-primary" onclick="camera_utils("startrecord")">Record</a>'
    html += '<a id="stopRecord" class="btn btn-primary" onclick="camera_utils("stoprecord")">Stop</a>'
    html += '</div><br>'
    html += '<div id="gallery_thumbnails"><p>'
    
    for thisline in linearray:
        justname = thisline.split('/')
        html += '<a href="'+thisline +'" rel="thumbnail"><img src="'+thisline+'" style="width: 50px; height: 50px" /></a>'
    html += '</p></div><br>'

    view.setContent('Live camera', html)
    output(view, cgi.FieldStorage())
    
if __name__ == '__main__':
    main()
