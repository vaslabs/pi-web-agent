#!/usr/bin/python
import sys
import os
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/cernvm-appliance-agent'
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/toolkit')
sys.path.append(os.environ['MY_HOME']+'/etc/config')
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/chrome')
from cern_vm import Configuration
from Adapter import GenericAdapter
from view import View
import cgi
import cgitb
cgitb.enable()

def main():
    '''
    generates an error page 
    '''
    config=Configuration()
    fs=cgi.FieldStorage()
    view = View(config.system.actions)
    view.setContent('Timeout error', 
        'We are sorry that a timeout occured. '+\
        'We probably know that this task takes time and ' +\
        'we are working to fix it!')
    view.output()
    
if __name__ == '__main__':
    main()
