#!/usr/bin/python
import cgi
import cgitb
import os
cgitb.enable()
import sys
sys.path.append(os.environ['MY_HOME']+'/objects')
sys.path.append(os.environ['MY_HOME']+'/etc/config')
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/chrome')
from PasswordManager import *
from cern_vm import Configuration
from view import View
from framework import output

def main():
    form = cgi.FieldStorage()
    config=Configuration()
    view = View(config.system.actions)
    if "passwd" not in form and "passwd_new1" not in form and "passwd_new2" not in form:
        view.setContent('User management', getView())
    else:
        pm = PasswordManager(form, 'admin')
        try:
            pm.doTransaction()
            view.setContent("User management", getSuccessView())
            
        except Exception as e:
            view.setContent("User management", getFailedView(e.strerror))

    output(view, form)
        
if __name__ == '__main__':
    main()
