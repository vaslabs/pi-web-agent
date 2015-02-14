#!/usr/bin/python
import sys
import os
import cgi
import cgitb

cgitb.enable()
sys.path.append(os.environ['MY_HOME']+'/cgi-bin')
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/chrome')
sys.path.append(os.environ['MY_HOME']+'/etc/config')
from framework import output, view, get_template


def get_view():
    with open(get_template("update_controller")) as template:
        return template.read()

    
def main():
    # Serves the update page
    fs = cgi.FieldStorage()
    content = get_view()
    view.setContent('Update', content)
    
    output(view, fs)
    
if __name__ == '__main__':    
    main()
