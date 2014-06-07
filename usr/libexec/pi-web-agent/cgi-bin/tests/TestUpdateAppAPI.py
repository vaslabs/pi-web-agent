import sys, os
import unittest
import PiWebAgentTestSuite
from update_api import *
class TestUpdateApp(unittest.TestCase):
    
    def test_update_data(self):
        updMgr = UpdateManagerAPI()
        state = updMgr.getJS() 
        print state
        self.assertTrue('packages' in state)
        
if __name__ == '__main__':
    unittest.main()
