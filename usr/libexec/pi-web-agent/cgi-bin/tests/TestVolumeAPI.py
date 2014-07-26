import sys, os
import unittest
import PiWebAgentTestSuite
from volume_api import *
class TestVolumeAPI(unittest.TestCase):
    
    def test_muted(self):
        data = json.loads(get_volume({'mixer':'PCM'}))
        print data['volume'], data['status']
        if int(data['volume']) == 0:
            self.assertTrue(not data['status'])
        else:
            self.assertTrue(data['status'])
            
    def test_speakers(self):
        test_speakers()
if __name__ == '__main__':
    unittest.main()
