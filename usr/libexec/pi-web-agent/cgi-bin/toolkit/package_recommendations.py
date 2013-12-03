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
from live_info import execute
'''
def checkError(view, errorcode) :
    if errorcode != 0 :
        view.setContent('Package Management', 'Something weird happened. . Try refreshing the page. .' )
        exit('Something weird happened')
'''
def main():
    '''
    Application to manage all the most used packages using apt-get.
    Unfinished.
    '''
    form = cgi.FieldStorage()
    
    sm=serviceManagerBuilder()
    config=Configuration()
    view = View(config.system.actions)

    htmlcode = ''

    ins = open( "recommendationsList.txt", "r" )
    packages = []
    for line in ins:
      line = line.rstrip() # strip the new line
      packages.append( line )

    allPackages = [[]]
    
    for pName in packages :
      checkedText = createOnOffSwitch( pName )
      descriptionText = getDpkgInfo( pName, "Description" )
      versionText = getDpkgInfo( pName, "Version" )
      allPackages.append( [ pName, checkedText, descriptionText, versionText ] )

    htmlcode += HTML.table( allPackages, header_row=['Package Name', 'Status', 'Description', 'Version'] )
    
    htmlcode += '<div id="overlay" >'
    htmlcode += '<div class="progress progress-striped active" style ="width: 400px; height: 80px; margin: auto; margin-top: 80px">'\
                +'<div class="progress-bar"  role="progressbar" aria-valuenow="100"'\
                +' aria-valuemin="0" aria-valuemax="100" style="width: 100%">'\
                +' <span class="sr-only">100% Complete</span>  </div></div></div>'


    view.setContent('Package Management', htmlcode )
    view.output()

def getDpkgInfo(pName, fieldName) :
    bashCommand = "./apt-query " + pName + " " + fieldName
    output, errorcode = execute( bashCommand )
    if output == "" :
      return fieldName + " not available"
    return output
        
def createOnOffSwitch( pName ) :
  checkedText = ""
  bashCommand = "dpkg-query -l | grep '" + pName + " '"
  output, errorcode = execute( bashCommand )
  #checkError(view, errorcode)

  text = '<div class="on_off_switch">\n'
  text +='<input type="checkbox" name="'+pName+'" onclick="submit_package(this)" class="on_off_switch-checkbox" id="'+pName 
  if output == "" :
    checkedText = text + '" checked>'
  else :
    checkedText = text + '">'
  checkedText += '<label class="on_off_switch-label" for="'+pName+'">\n'
  checkedText += '<div class="on_off_switch-inner"></div>\n'
  checkedText += '<div class="on_off_switch-switch"></div>\n'
  checkedText += '</label>\n'
  checkedText += '</div>\n'
  return checkedText

if __name__ == '__main__':
    main()
    
