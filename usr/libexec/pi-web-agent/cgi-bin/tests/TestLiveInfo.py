import sys, os
import unittest
import PiWebAgentTestSuite
from live_info import package_is_installed
class TestLiveInfo(unittest.TestCase):
    
    def test_package_is_installed(self):
        self.assertTrue(package_is_installed('apache2'))
        self.assertTrue(not package_is_installed('scala'))
        
if __name__ == '__main__':
    unittest.main()
