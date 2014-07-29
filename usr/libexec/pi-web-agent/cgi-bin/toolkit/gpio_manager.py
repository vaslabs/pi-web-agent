#!/usr/bin/python
import cgi, cgitb
import os, sys
cgitb.enable()
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME']+'/etc/config')
sys.path.append(os.environ['MY_HOME']+'/cgi-bin')
from framework import view, output, get_template
from HTMLPageGenerator import composeJS
from live_info import execute

gpio="/usr/local/bin/gpio"

def main():
    form = cgi.FieldStorage()
    
    f = open(get_template('gpio_controller'))
    html_tables= f.read()
    f.close()

    view.setContent('GPIO Controller', html_tables)
    output(view, form)
    
    
if __name__ == '__main__':
    main()
