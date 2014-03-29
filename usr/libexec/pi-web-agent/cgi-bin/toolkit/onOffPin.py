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
cgitb.enable()
from live_info import execute

gpio="/usr/local/bin/gpio"

def set_pin_value(pin_no, value):
    command="sudo " + gpio + " write " + str(pin_no) + " " + value
    return execute(command.replace("\n", "")) #protect command from newlines
    
def set_pin_direction(pin_no, direction):
    command = "sudo " + gpio + " mode " + str(pin_no) + " " + direction
    return execute(command.replace("\n", ""))


def main():
    form = cgi.FieldStorage()
    msg=""
    if 'cmd' in form:
        command=form['cmd'].value
        if (command=='cleanup'):
            msg, errorcode=execute("sudo " + gpio + " reset")
        else:
            errorcode="140"
    else:
        pinID = form['id'].value
        pinTypeOfChange = pinID.split('GPIO')[0]
        pinName = form['pinNumber'].value
        pinNo = pinName.split('GPIO')[1]
        wiringPiIndex, err = execute("sudo gpio-query wiringpi \"GPIO " + str(pinNo) + "\"")
    
        pinNo = wiringPiIndex
        errorcode = None

        if pinTypeOfChange == 'V' :
            pinValue = form['value'].value
            msg, errorcode = set_pin_value(pinNo, pinValue)
        elif pinTypeOfChange == 'D' :
            pinDirection = form['direction'].value
            msg, errorcode = set_pin_direction(pinNo, pinDirection)
        else:
            msg="Uknown command"
            errorcode="130"
    response = Response(errorcode)
    
    response.buildResponse(errorcode, message=msg)
    composeXMLDocument(response.xml)

if __name__ == '__main__':
    main()
