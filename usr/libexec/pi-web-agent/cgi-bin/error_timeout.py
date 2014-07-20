#!/usr/bin/python
import sys
import os
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/cernvm-appliance-agent'
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/toolkit')
sys.path.append(os.environ['MY_HOME']+'/etc/config')
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/chrome')

import cgi
import cgitb
cgitb.enable()
from framework import view, output

def main():
    '''
    generates an error page 
    '''
    fs=cgi.FieldStorage()
    view.setContent('Timeout error', 
        'We are sorry that a timeout occured. '+\
        'We probably know that this task takes time and ' +\
        'we are working to fix it!')
    output(view, fs)
    
if __name__ == '__main__':
    main()
