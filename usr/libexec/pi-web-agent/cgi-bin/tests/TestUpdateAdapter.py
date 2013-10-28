#!/usr/bin/python
import sys
import os
sys.path.append('/var/cernvm-www/cgi-bin/toolkit')
import UpdateAdapter
from UpdateAdapter import *
import unittest

class TestHTMLPageGenerator(unittest.TestCase):

    def setUp(self):
        self.updateAdapter = UpdateAdapter()

    def test_update(self):
        message=self.updateAdapter.message()
        sysupdate=os.system('cat ../update_file')
        if sysupdate == 0:
            self.assertEqual(message, UPDATE_OK)
            
        elif sysupdate == 100:
            self.assertEqual(message, UPDATE)
            
        elif sysupdate == 1:
            self.assertEqual(message, UPDATE_ERROR)
        else:
            self.fail("Uknown code from yum")
            

    def test_update_view(self):
        self.assertTrue(len(self.updateAdapter.generateHtmlView()) > 0, "Take a look at the text")
        

if __name__ == '__main__':
    unittest.main()
