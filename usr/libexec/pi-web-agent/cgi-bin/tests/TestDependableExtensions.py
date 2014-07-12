import sys, os
import unittest
import PiWebAgentTestSuite
from vnc import VNCManager
from mplayer import MediaPlayerManager
from DependableExtension import DependableExtension
class TestDependableExtensions(unittest.TestCase):
    
    def test_vnc_dependency(self):
        vnc = VNCManager()
        self.assertTrue(not vnc.check_status())
        mpm = MediaPlayerManager()
        self.assertTrue(not mpm.check_status())
        
if __name__ == '__main__':
    unittest.main()
