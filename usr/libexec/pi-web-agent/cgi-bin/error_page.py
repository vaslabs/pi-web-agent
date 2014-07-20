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
    view.setContent('Page not found', 'The requested page was not found. Did you type the url manually?')
    output(view, fs)
if __name__ == '__main__':
    main()
