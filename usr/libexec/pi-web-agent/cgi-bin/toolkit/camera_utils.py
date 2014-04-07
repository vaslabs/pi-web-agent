#!/usr/bin/python

import sys
import os
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME'] + '/cgi-bin')
sys.path.append(os.environ['MY_HOME'] + '/cgi-bin/toolkit')
sys.path.append(os.environ['MY_HOME'] + '/cgi-bin/chrome')
sys.path.append(os.environ['MY_HOME'] + '/etc/config')
sys.path.append(os.environ['MY_HOME'] + '/objects')
sys.path.append(os.environ['MY_HOME'] + '/cgi-bin/api')
import cgi
import cgitb
from cernvm import Response
from live_info import execute
from HTMLPageGenerator import *

MY_PICS="/usr/share/pi-web-agent/my_pics"

def takeSnapshot( ):
    return execute( "sudo raspistill -t 2000 -o " + MY_PICS + "/image1.jpg" )

def getCameraStatus( ):
    return execute( "sudo vcgencmd get_camera" )

def enableCamera( ):
    return execute( os.environ['MY_HOME'] + "/scripts/camera_enable.sh" )

def stopRecord( ):
    return 

def startRecord( ):
    return 
    
def play( ):
    return 

def main():

    form = cgi.FieldStorage()
    cameraAction = form['action'].value
    output = ''
    if cameraAction == 'snapshot' :
      output, errorcode = takeSnapshot()
    elif cameraAction == 'play' :
      output, errorcode = play()
    elif cameraAction == 'startrecord' :
      output, errorcode = startRecord()
    elif cameraAction == 'stoprecord' :
      output, errorcode = stopRecord()
  

    response = Response(0)
        
    response.buildResponse(errorcode)
    composeXMLDocument(response.xml)

if __name__ == '__main__':
    main()
