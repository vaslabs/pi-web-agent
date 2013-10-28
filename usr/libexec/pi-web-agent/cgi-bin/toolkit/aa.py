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
    return output

def main():
    '''
    Application to manage all the most used packages using apt-get.
    Unfinished.
    '''
    form = cgi.FieldStorage()
    
    sm=serviceManagerBuilder()
    config=Configuration()
    view = View(config.system.actions)
    
    table_data = [
            ['Smith',       'John',         30],
            ['Carpenter',   'Jack',         47],
            ['Johnson',     'Paul',         62],
        ]

    htmlcode = HTML.table(table_data,
        header_row=['Last name',   'First name',   'Age'])

    ins = open( "recommendationsList.txt", "r" )
    packages = []
    for line in ins:
        packages.append( line )

    installedPackages = [[]]
    toInstallPackages = [[]]
    
    i = -1
    j = -1
    for a in packages:
        a = a.rstrip() # strip the new line
        bashCommand = "dpkg-query -l | grep '" + a + " '"
        output = execute( bashCommand )
        if output == "" :
            i += 1
            toInstallPackages.append( [a, 'w8'] )
        else :
            j += 1
            installedPackages.append( [ a, 'w8'] )

    if i != -1 :
        htmlcode += HTML.table( toInstallPackages,
            header_row=['Package Name', 'p'] )

    if j != -1 :
        htmlcode += HTML.table( installedPackages,
            header_row=['Package Name', 'p'] )
        

        #if installed add it in the installedPackages array
        #else in the restPackages
#subprocess.call("./checkIfInstalled.sh", shell=True)\ -> maybe generate xml file to get response so it is then compatible with the android
        
    view.setContent('Arxidi2 App', htmlcode )
    view.output()


if __name__ == '__main__':
    main()
    
