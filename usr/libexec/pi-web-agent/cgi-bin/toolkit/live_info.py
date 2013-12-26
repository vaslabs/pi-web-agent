#!/usr/bin/python
import os
import sys
import subprocess
import cgi
import cgitb
import xml.etree.ElementTree as ET
from services import *
cgitb.enable()
NO_ACTION=0
UPDATE_READY=101
NEW_UPDATE=110
REBOOT_REQUIRED=120
UPDATE_PENDING=100
DPKG_CONFIG_NEEDED=200
PROCESS_RUNNING=201

if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME']+'/cgi-bin')
from HTMLPageGenerator import *

def execute(command):
    
    sp=subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = sp.communicate()
    sp.wait()
    return [output, sp.returncode]

def getMemoryUsage():
    command=os.environ['MY_HOME'] + '/scripts/memory_information MemFree'
    free=execute(command)[0]
    command=os.environ['MY_HOME'] + '/scripts/memory_information MemTotal'
    total=execute(command)[0]
    return 100 - int((float(free)/float(total))*100)

def getDiskUsage():
    command='df -hP / | grep -o -w -E \'[0-9]*\%\' | tr -d \'%\''
    return execute(command)[0]
        
def swapUsage():
    command=os.environ['MY_HOME'] + '/scripts/memory_information SwapFree'
    free=execute(command)[0]
    command=os.environ['MY_HOME'] + '/scripts/memory_information SwapTotal'
    total=execute(command)[0]
    if free == None or len(str(free)) == 0 or int(total) == 0:
        return -1
    return 100 - int((float(free)/float(total))*100)

def getKernelVersion():
    command='uname -r'
    return execute(command)[0]

def hostname():
    command = os.environ['MY_HOME'] + '/scripts/hostname.sh'
    return execute(command)[0]
    
def update_check():
    command = 'sudo pi-update -c'
    return execute(command)
    
def update_check_quick():
    command = 'sudo pi-update -q'
    return execute(command)
        
def update_check_js():
    command = 'sudo pi-update -q'
    a=execute(command)
    return a[1] == NEW_UPDATE

def response(msg):
    element=ET.Element('response')
    element.text=msg
    composeXMLDocument(element)
    
def update_check_with_version():
    command = 'sudo pi-update -c'
    a=execute(command)
    response=a[1]
    return [response == NEW_UPDATE, a[0]]

def turn_service(service_name, turn):
    if (turn == "on"):
        newturn = "start"
    else:
        newturn = "stop"
    command='sudo service ' + service_name + ' ' + newturn    
    a=execute(command)
    
    return a[1]

def get_temperature():
    command='sudo /opt/vc/bin/vcgencmd measure_temp'
    output, exit_code = execute(command)
    if not exit_code == 0:
        return 'N/A'
    else:
        degrees_in_celcius=output.split('=')[1].split("'")[0]
        return degrees_in_celcius

def manage_vnc(turn):
    command = 'sudo /etc/init.d/vncboot ' + turn
    output, errcode = execute(command)

def main():
    cmds = {'mem':getMemoryUsage, 'kernel':getKernelVersion,\
     'disk': getDiskUsage, 'swap':swapUsage, 'hostname':hostname,\
     'update':update_check_js, 'edit_service':turn_service, 'temp':get_temperature}
    fs = cgi.FieldStorage()
    if 'cmd' not in fs or fs['cmd'].value not in cmds.keys():
        response('Error')
    else:
        if 'param1' in fs and 'param2' in fs:
            response(str(cmds[fs['cmd'].value](fs['param1'].value, fs['param2'].value)))        
        else:
            response(str(cmds[fs['cmd'].value]()))  


if __name__ == '__main__':
    main()    
    
