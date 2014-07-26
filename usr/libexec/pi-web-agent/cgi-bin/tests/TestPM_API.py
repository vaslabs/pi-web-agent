import sys, os
import unittest
import PiWebAgentTestSuite
from pm_api import *
class TestPMAPI(unittest.TestCase):
    
    def test_PM_search(self):
        result = search_package({'key':'apt-get'})
        self.assertTrue(type(result) is dict)
        self.assertTrue('apt' in result)
        self.assertTrue('\n' not in result)
        
    def test_PM_search_dummy(self):
        result = search_package({'key':'jfoariowe'})
        self.assertTrue(result == {})
        
    def test_check_if_package_is_installed(self):
        result = check_installed({'key':'apt'})
        self.assertTrue(result['installed'])
        result = check_installed({'key':'ruby'})
        self.assertFalse(result['installed'])
        
if __name__ == '__main__':
    unittest.main()
