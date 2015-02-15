#!/usr/bin/python
import sys
import os
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME'] + '/cgi-bin')
sys.path.append(os.environ['MY_HOME'] + '/cgi-bin/toolkit')
sys.path.append(os.environ['MY_HOME'] + '/cgi-bin/chrome')
sys.path.append(os.environ['MY_HOME'] + '/etc/config')
sys.path.append(os.environ['MY_HOME']+'/objects')
import cgi
import cgitb
from subprocess import Popen, PIPE
cgitb.enable()
from live_info import execute, getAptBusy
from framework import output, view
from view import composeJS
import json

PACKAGES_LIST_PATH=\
"/usr/libexec/pi-web-agent/etc/config/pm/recommendationsList.txt"
STOP = {'STOP': 'There are no more packages to load'}
        
def checkFlags(pName):
    bashCommand = "dpkg-query -l " + pName
    text, errorcode = execute( bashCommand )
    if errorcode != 0:
        return False
    lines = text.split('\n')
    del lines[-1]
    package_line = lines[-1]
    flags = package_line.split()[0]
    if flags.find('r') >= 0:
        return False
    if flags.find('un') >= 0:
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
        installed = checkFlags(pName)
        descriptionText = getDpkgInfo( pName, "Description" )
        versionText = getDpkgInfo( pName, "Version" )
        package = {'Package Name':pName, 'Description':descriptionText, 'Version':versionText, 'installed':installed}    

        allPackages.append( package )

    return allPackages

def main():
    form = cgi.FieldStorage()

    if('index' in form and form['index'].value != -1 ) :
      packages = getTableRecord( form['index'].value )
      if packages != None :
        composeJS( json.dumps( packages ) )
      else :
        composeJS( json.dumps( STOP ) )
    elif ('op' in form and form['op'].value == 'status'):          
        composeJS(json.dumps({'status':not getAptBusy()}))
    else:
        composeJS(json.dumps({}))    

if __name__ == '__main__':
    main()

