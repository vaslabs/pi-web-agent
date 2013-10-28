#!/usr/bin/python
import cgi
import crypt
import sys
import os
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/cernvm-appliance-agent'
sys.path.append(os.environ['MY_HOME'] + '/cgi-bin')
from HTMLPageGenerator import *
from BlueprintDesigner import *
import subprocess

def getView():
    iwpasswd = InputWidget('password', 'passwd', '', 'Current password: ',wClass='form-control password',attribs='placeholder="Current Password"')
    iwpasswd_new1=InputWidget('password', 'passwd_new1', '', 'Set new Password: ',wClass='form-control password',attribs='placeholder="New Password"')
    iwpasswd_new2=InputWidget('password', 'passwd_new2', '', 'Retype password: ',wClass='form-control password',attribs='placeholder="Retype Password"')
    iw_submit=InputWidget('button', '', 'Change password', '',wClass='btn btn-primary')
    iwg = InputWidgetGroup()
    iwg.widgets=[iwpasswd, iwpasswd_new1, iwpasswd_new2, iw_submit] 
    return fieldset('/cgi-bin/toolkit/change_password.py', 'POST', 'password_form', iwg, createLegend("Change password"))


def getSuccessView():
    message="Password has changed successfully"
    return createDiv(message, 'success')

def getFailedView(errorMessage):
    message="Password did not change: " + errorMessage
    return createDiv(message, 'error') 

class PasswordManager(object):

    '''
    PasswordManager manages the .htpasswd file through
    the htpasswd program. It checks for a valid current
    password and validates the new password
    '''
    def __init__(self, form, username=None):
        if (username==None):
            self.username = form.getvalue('username')
        else:
            self.username = username
        self.form = form
        
        
    def doTransaction(self):
        '''
        stores the password if the usual password validity conditions are met.
        '''
        self.password=self.form.getvalue("passwd")
        self.password1=self.form.getvalue("passwd_new1")
        self.password2=self.form.getvalue("passwd_new2")    
        if (self.password1 != self.password2):
            e=Exception()
            e.strerror="Passwords mismatch"
            raise e
        if (not self._check()):
            e=Exception()
            e.strerror="Wrong username/password"
            raise e    
        #passed all checks, now safely store password
        self._store()
        
        
    def _store(self):
        pFile = os.environ['MY_HOME'] + '/.htpasswd'
        if "'" in self.username or "'" in self.password1:
            e=Exception()
            e.strerror="Invalid character `'` in password"
            raise e        
        command = 'sudo htpasswd -bd ' + pFile + ' \'' + self.username + '\' ' + ' \'' + self.password1 +'\''
        sp=subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        output, _ = sp.communicate()
	
        sp.wait() 
		
    def _check(self):
 
        content_file = open(os.environ['MY_HOME']+'/.htpasswd', 'r')
        for line in content_file:
            data = line.rstrip(' \n').split(':')
            if (data[0]==self.username):
                break
        if (data[0] != self.username):
            e=Exception("Wrong username/password")
            e.strerror="Wrong username/password"
            raise e
        content_file.close()    
        user=data[0]
        encrPass=data[1]
        self.salt=encrPass[0:2]
        if crypt.crypt(self.password, self.salt) == encrPass and user==self.username:
            return True
        return False
