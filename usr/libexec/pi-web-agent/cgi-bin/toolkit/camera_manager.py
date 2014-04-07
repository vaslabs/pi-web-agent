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

def main():

    form = cgi.FieldStorage()
    
    pictures, returncode = execute("ls /usr/share/pi-web-agent/camera-media/*.jpg")
    linearray = pictures.split('\n')
    
    html = '<div id="camera_toolbar">\n'
    html += '<a id="makePreview" class="btn btn-primary" onclick=\'camera_utils("play")\'>Play</a>'
    html += '<a id="takeSnapshot" class="btn btn-primary" onclick=\'camera_utils("snapshot")\'>Snapshot</a>'
    html += '<a id="startRecord" class="btn btn-primary" onclick=\'camera_utils("startrecord")\'>Record</a>'
    html += '<a id="stopRecord" class="btn btn-primary" onclick=\'camera_utils("stoprecord")\'>Stop</a>'
    html += '</div><br>'
    html += '''<div id="gallery_thumbnails"<p>'''
    
    for thisline in linearray:
        justname = thisline.split('/')[-1]
        if len(justname) <= 0:
            continue
        html += '<a href="/cgi-bin/toolkit/image_manager.py?image='+justname +'" rel="thumbnail"><img style="padding:4px; border:2px solid #021a40;" src="/cgi-bin/toolkit/image_manager.py?image='+justname.split('.')[0]+'.png" style="width: 64px; height: 64px" /></a>'
    html += '</p></div><br>'

    view.setContent('Live camera', html)
    output(view, cgi.FieldStorage())
    
if __name__ == '__main__':
    main()
