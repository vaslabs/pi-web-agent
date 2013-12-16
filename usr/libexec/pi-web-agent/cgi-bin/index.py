#!/usr/bin/python
import sys
import os
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/chrome')
sys.path.append(os.environ['MY_HOME']+'/etc/pi-web-agent/config')
sys.path.append(os.environ['MY_HOME']+'/usr/libexec/pi-web-agent/scripts')
from menu import *
from view import View
from cern_vm import Configuration

import cgi
import crypt
def main():
    if password_changed():
        config = Configuration()
        indexView=View(config.system.actions)
        indexView.output()
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
    
