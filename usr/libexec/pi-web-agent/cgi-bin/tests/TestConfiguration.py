#!/usr/bin/python
import sys, os
import unittest
import PiWebAgentTestSuite
from pi_web_agent import Configuration

class TestConfiguration(unittest.TestCase):
		

	def test_configuration(self):
	    config = Configuration()
	    self.assertEqual(config.system.cmdactions['System Information']['title'],'System Information')
	    self.assertEqual(config.system.cmdactions['Scheduled Tasks']['title'],'Scheduled Tasks')
	    self.assertEqual(config.system.cmdactions['Running Processes']['title'],'Processes')
	    self.assertTrue(len(config.system.actions) > 1)
	    
	    
	    

if __name__ == '__main__':
    unittest.main()
