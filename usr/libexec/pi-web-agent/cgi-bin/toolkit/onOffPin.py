#!/usr/bin/python
import sys, os
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/api')
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/')
from HTMLPageGenerator import *
from cernvm import Response
import cgi
import cgitb
from subprocess import Popen, PIPE

cgitb.enable()

from live_info import execute

def set_pin_value(pin_no, value):
	msgValue, errorcode=execute("sudo sh -c 'echo \""+ value +" \" > /sys/class/gpio/gpio" + pin_no + "/value'")
	return errorcode
	
def set_pin_direction(pin_no, direction):
	msgDirection, errorcode=execute("sudo sh -c 'echo \""+ direction +" \" > /sys/class/gpio/gpio" + pin_no + "/direction'")
	return errorcode

def main():
    form = cgi.FieldStorage()
	pinID = form['id'].value
	pinTypeOfChange = pinID.split('GPIO')[0]
	pinName = form['pinName'].value
	pinNo = pinName.split('GPIO')[1]
	
	errorcode = None
	if pinTypeOfChange == 'V' :
		pinValue = form['value'].value
		errorcode = set_pin_value(pinNo, pinValue)
	elif pinTypeOfChange == 'D' :
		pinDirection = form['direction'].value
		errorcode = set_pin_direction(pinNo, pinDirection)

    response = Response(0)
	
    response.buildResponse(errorcode)
    composeXMLDocument(response.xml)
if __name__ == '__main__':
    main()
