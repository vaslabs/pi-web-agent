#!/usr/bin/python
import sys
import os
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/chrome')
sys.path.append(os.environ['MY_HOME']+'/etc/pi-web-agent/config')
sys.path.append(os.environ['MY_HOME']+'/usr/libexec/pi-web-agent/scripts')
from menu import *
from view import View
from cern_vm import Configuration

import cgi
import crypt

MAIN_VIEW = os.environ['MY_HOME'] + '/etc/config/main_view.html'

def main():
    if password_changed():
        config = Configuration()
        view=View(config.system.actions)
        main_view_file = open(MAIN_VIEW)
        content = main_view_file.read()
        main_view_file.close()
        view.setContent('Welcome', content)
        view.output()
    else:
        redirect()

def password_changed():
    default_username='admin'
    default_password='admin'
    content_file = open(os.environ['MY_HOME']+'/.htpasswd', 'r')
    for line in content_file:
        data = line.rstrip(' \n').split(':')
        if (data[0]==default_username):
            break
    content_file.close()    
    user=data[0]
    encrPass=data[1]
    salt=encrPass[0:2]
    if crypt.crypt(default_password, salt) == encrPass and user==default_username:
        return False
    return True

def redirect():
    
  print 'Content-Type: text/html'
  print 
  print '<html>'
  print '  <head>'
  print '    <meta http-equiv="refresh" content="0;url=/cgi-bin/toolkit/change_password.py" />'
  print '    <title>You are going to be redirected to change your password</title>'
  print '  </head>' 
  print '  <body>'
  print '    Redirecting... <a href="/cgi-bin/index.py">Click here if you are not redirected</a>'
  print '  </body>'
  print '</html>'

main()
    
