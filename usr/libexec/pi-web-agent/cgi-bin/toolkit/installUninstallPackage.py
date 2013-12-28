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


def installPackage(pName):
    return execute( "sudo pi-package-management --install " + pName )

def uninstallPackage(pName):
    return execute( "sudo pi-package-management --remove " + pName )

def main():
    form = cgi.FieldStorage()
    #form={'action':'uninstall', 'packageName':'tree'}
    pName = form['packageName'].value
    output = ''
    if form['action'].value == 'install' :
        output, errorcode = installPackage(pName)
    elif form['action'].value == 'uninstall' :
        output, errorcode = uninstallPackage(pName)

    response = Response(0)
        
    response.buildResponse(errorcode)
    composeXMLDocument(response.xml)
if __name__ == '__main__':
    main()
