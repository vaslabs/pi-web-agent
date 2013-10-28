#!/usr/bin/python
import sys
sys.path.append('/etc/cernvm-applicance-agent/config')
import unittest
from cern_vm import Configuration

class TestConfiguration(unittest.TestCase):
		

	def test_configuration(self):
	    configManager = Configuration()
	    self.assertEqual(configManager.system.actions[0].title,'Status')
	    self.assertEqual(configManager.system.actions[0].id,'Appliance Status')
	    self.assertEqual(configManager.system.actions[0].url,'toolkit/status')
	    #test with extension, comment out if extension does not exist
	    self.assertEqual(configManager.system.actions[3].title, 'StatusE')
	    self.assertEqual(configManager.system.actions[3].id, 'Appliance StatusE')
	    self.assertEqual(configManager.system.actions[3].url, 'toolkit/statusE')          	        

if __name__ == '__main__':
    unittest.main()
