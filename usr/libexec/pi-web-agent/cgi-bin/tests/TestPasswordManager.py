#!/usr/bin/python
import sys
import unittest
import os
sys.path.append(os.environ['CVM_AA_CONFIG_PATH'])
sys.path.append(os.environ['CVM_AA_APP_PATH'] + '/scripts')
from PasswordManager import *

class TestHTMLPageGenerator(unittest.TestCase):

	def setUp(self):
		self.username="admin"
		self.password=raw_input('Current password: ')
		self.password1=raw_input('New password: ')
		self.password2=raw_input('Retype new password: ')
		self.form=TestForm()
		self.form.add('passwd', self.password)
		self.form.add('passwd_new1', self.password1)
		self.form.add('passwd_new2', self.password2)
		pm = PasswordManager(self.form, self.username)

	#def test_radio_widget(self):
	 #   pm.doTransaction()
	    
	def test_views(self):
	    print getView()
	    print getSuccessView()
	    print getFailedView("Exception message")
        
#clone for web form just for testing
class TestForm:
    
    def __init__(self):
        self.attribs={}
    
    def add(self, key, value):
        self.attribs[key]=value
    
    def getvalue(self, key):
        return self.attribs[key]    

if __name__ == '__main__':
    unittest.main()
