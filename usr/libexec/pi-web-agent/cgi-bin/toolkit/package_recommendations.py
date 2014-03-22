#!/usr/bin/python
import sys
import os
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME'] + '/cgi-bin')
sys.path.append(os.environ['MY_HOME'] + '/cgi-bin/toolkit')
sys.path.append(os.environ['MY_HOME'] + '/cgi-bin/chrome')
sys.path.append(os.environ['MY_HOME'] + '/etc/config')
from services import *
from view import *
from cern_vm import Configuration
import cgi
import cgitb
from subprocess import Popen, PIPE
import HTML
cgitb.enable()
from live_info import execute, getAptBusy
from framework import output
from HTMLPageGenerator import *
import json

PACKAGES_LIST_PATH=\
"/usr/libexec/pi-web-agent/etc/config/pm/recommendationsList.txt"
STOP = {'STOP': 'There are no more packages to load'}
        
def checkFlags(text):
    lines = text.split('\n')
    del lines[-1]
    package_line = lines[-1]
    flags = package_line.split()[0]
    if flags.find('r') >= 0:
        return False
    return True
    
def isInt(s):
  try:
    int(s)
  except exceptions.ValueError:
    return -1

def getDpkgInfo(pName, fieldName) :
    bashCommand = "apt-query " + pName + " " + fieldName
    output, errorcode = execute( bashCommand )
    if output == "" :
      return fieldName + " not available"
    return output
        
def createOnOffSwitch( pName ) :
    checkedText = ""
    bashCommand = "dpkg-query -l " + pName
    output, errorcode = execute( bashCommand )

    text = '<div class="on_off_switch">\n'
    text +='<input type="checkbox" name="'+pName+'" onclick="submit_package(this)" class="on_off_switch-checkbox" id="'+pName 
    if errorcode != 0:
        checkedText = text + '" checked>'
    elif errorcode == 0 and checkFlags(output):
        checkedText = text + '">'
    else:
        checkedText = text + '" checked>'
    checkedText += '<label class="on_off_switch-label" for="'+pName+'">\n'
    checkedText += '<div class="on_off_switch-inner"></div>\n'
    checkedText += '<div class="on_off_switch-switch"></div>\n'
    checkedText += '</label>\n'
    checkedText += '</div>\n'
    return checkedText


def getTableRecord( index ) :
    
    if( isInt( index ) == -1 ) :
      return ''
    index = int( index )

    ins = open( PACKAGES_LIST_PATH, "r" )
    packages = []
    counter = 0
    for line in ins :
      counter += 1
      if( counter == index ) :
        line = line.rstrip( ) # strip the new line
        packages.append( line )
      
    if( len(packages) == 0 ) :
      return None
    
    htmlcode = ''  
    allPackages = []

    for pName in packages :
        checkedText = createOnOffSwitch( pName )
        descriptionText = getDpkgInfo( pName, "Description" )
        versionText = getDpkgInfo( pName, "Version" )
        package = {'Package Name':pName, 'Status':checkedText, 'Description':descriptionText, 'Version':versionText}    

        allPackages.append(package)

    return allPackages

def main():
    '''
    Application to manage the most used packages using apt-get.
    Unfinished.
    '''
    config=Configuration()
    view = View(config.system.actions)
    form = cgi.FieldStorage()

    if('index' in form and form['index'].value != -1 ) :
      packages = getTableRecord( form['index'].value )
      if packages != None :
        composeJS( json.dumps(packages) )
      else :
        composeJS( json.dumps( STOP ) )
    else :
      if ( getAptBusy( ) ):
        view.setContent('Package Management',\
        '<script src="/css/reloadBasedOnStatus.js"></script>\
        The package manager is busy right now. . . \
        This page will automatically reload once the service is available')
        output(view, form)
      else :
        htmlcode = "\n<div id='packages-table'><table id='packages-table-id'>"
        htmlcode += "\n</table></div>"
        view.setContent('Package Management',\
        '<script src="/css/lazyLoading.js"></script>' + htmlcode )
        output(view, form)  
   
if __name__ == '__main__':
    main()
    
