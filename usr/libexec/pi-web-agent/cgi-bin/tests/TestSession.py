#!/usr/bin/python
import sys
sys.path.append('/var/cernvm-www/cgi-bin')
from session import Session
import unittest

class TestSession(unittest.TestCase):
    
    def setUp(self):
        self.session=Session()
    
    def test_correct_authentication(self):
        username='admin'
        password='admin'
        self.session.newSession(username, password)
        self.assertTrue(self.session.check())
        
    def test_wrong_authentication(self):
        username='admin'
        password='whatever'
        self.session.newSession(username, password)
        self.assertFalse(self.session.check())
        username='hello'
        password='admin'
        self.session.newSession(username, password)
        self.assertFalse(self.session.check())

    def test_password_visibility(self):
        try:
            print self.session._password
            self.fail()
        except:
            pass

def main():    
    unittest.main()
        
main()
