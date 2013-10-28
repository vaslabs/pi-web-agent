#!/usr/bin/python
import sys
import os
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/cernvm-appliance-agent'
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

def execute(command):
    sp=subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = sp.communicate()
    sp.wait()
    return output, err
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
        packages.append( line )

    installedPackages = [[]]
    toInstallPackages = [[]]
    allPackages = [[]]
    
    i = -1
    j = -1
    for pName in packages:
        pName = pName.rstrip() # strip the new line
        bashCommand = "dpkg-query -l | grep '" + pName + " '"
        output, errorcode = execute( bashCommand )
        #checkError(view, errorcode)

        text = '<div class="on_off_switch">\n'
        text +='<input type="checkbox" name="'+pName+'" onclick="submit_package(this)" class="on_off_switch-checkbox" id="'+pName 
        if output == "" :
            i += 1
            checkedText = text + '" checked>'
        else :
            j += 1
            checkedText = text + '">'
        checkedText += '<label class="on_off_switch-label" for="'+pName+'">\n'
        checkedText += '<div class="on_off_switch-inner"></div>\n'
        checkedText += '<div class="on_off_switch-switch"></div>\n'
        checkedText += '</label>\n'
        checkedText += '</div>\n'
        allPackages.append( [ pName, checkedText ] )

    if i != -1 or j != -1 :
        htmlcode += HTML.table( allPackages,
            header_row=['Package Name', 'Status'] )
    
    htmlcode += '<div id="overlay" >'
    htmlcode += '<div class="progress progress-striped active" style ="width: 400px; height: 80px; margin: auto; margin-top: 80px">'\
                +'<div class="progress-bar"  role="progressbar" aria-valuenow="100"'\
                +' aria-valuemin="0" aria-valuemax="100" style="width: 100%">'\
                +' <span class="sr-only">100% Complete</span>  </div></div></div>'


    view.setContent('Package Management', htmlcode )
    view.output()


if __name__ == '__main__':
    main()
    
