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
    view.setContent('Page not found', 'The requested page was not found. Did you type the url manually?')
    view.output()
    
if __name__ == '__main__':
    main()
