import sys, os
import unittest
import PiWebAgentTestSuite
from vnc import VNCManager
from DependableExtension import DependableExtension
class TestDependableExtensions(unittest.TestCase):
    
    def test_vnc_dependency(self):
        vnc = VNCManager()
        self.assertTrue(vnc.check_status())
        
        
if __name__ == '__main__':
    unittest.main()
