import sys, os
import unittest
import PiWebAgentTestSuite
from camera_manager import CameraManager
from camera_manager_api import *

class TestCameraController(unittest.TestCase):
    
    def test_camera_manager_get_images(self):
        cMgr = CameraManager()
        json_data = cMgr.getImages()
        self.assertTrue(type(json_data) is list)
    
    def test_camera_manager_get_normal_view(self):
        cMgr = CameraManager()
        print cMgr.getNormalView()
        
if __name__ == '__main__':
    unittest.main()
