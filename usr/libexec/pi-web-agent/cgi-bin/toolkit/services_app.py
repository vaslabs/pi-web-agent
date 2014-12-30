#!/usr/bin/python
import sys
import os
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME'] + '/cgi-bin')
sys.path.append(os.environ['MY_HOME'] + '/cgi-bin/toolkit')
sys.path.append(os.environ['MY_HOME'] + '/cgi-bin/chrome')
sys.path.append(os.environ['MY_HOME'] + '/etc/config')

sys.path.append(os.environ['MY_HOME'] + '/objects')
from services import *
import cgi
import cgitb
cgitb.enable()
from framework import output, view, get_template
def main():
    '''
    Services application to manage levels of each service.
    It will support only enable/disable for a service.
    Unfinished.
    '''
    form = cgi.FieldStorage()
    
    f = open(get_template('services_controller'))
    html_tables= f.read()
    f.close()
    
    view.setContent('Services Management App', html_tables)
    output(view, form)

if __name__ == '__main__':
    main()
    
