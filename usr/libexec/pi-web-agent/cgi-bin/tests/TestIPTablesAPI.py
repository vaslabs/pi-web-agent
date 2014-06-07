import sys, os
import unittest
import PiWebAgentTestSuite
from pi_iptables_api import *

class TestIPTablesAPI(unittest.TestCase):
    
    def test_iptables_data(self):
        updMgr = UpdateManagerAPI()
        chain = updMgr.getJS() 
        print chain
        self.assertTrue('FORWARD' in chain)
        self.assertTrue('INPUT' in chain)
        self.assertTrue('OUTPUT' in chain)
        
if __name__ == '__main__':
    unittest.main()
