#!/usr/bin/python
import sys
import os
import cgi
import cgitb

cgitb.enable()
sys.path.append(os.environ['MY_HOME']+'/cgi-bin')
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/chrome')
sys.path.append(os.environ['MY_HOME']+'/etc/config')
from framework import output, view
from BlueprintDesigner import *
from HTMLPageGenerator import *
from volume_controller import get_volume


def get_view():
    vol = get_volume()
    content = "Current volume is: " + vol

    return content
    
def main():
    fs = cgi.FieldStorage()
    content = get_view()
    view.setContent('Volume manager', content)
    
    output(view, fs)
    
if __name__ == '__main__':    
    main()
