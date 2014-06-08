import sys, os
import unittest
import PiWebAgentTestSuite
from gpio_manager_api import *

class TestUpdateApp(unittest.TestCase):
    
    def test_update_data(self):
        main()
        
if __name__ == '__main__':
    unittest.main()
