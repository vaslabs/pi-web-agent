import sys, os
import unittest
import PiWebAgentTestSuite
from startup_manager import StartupManager
class TestStartupMgr(unittest.TestCase):
    
    def test_set_startup_defs(self):
        
        sMgr = StartupManager()
        result = sMgr.setStartupDefinition('python', '')
        self.assertTrue(result['code'] == 0)
        result = sMgr.setStartupDefinition('true', '')
        self.assertTrue(result['code'] == 0)
        
    def test_api_syntax(self):
        import startup_manager_api
        
    def test_rm_startup_def(self):
        sMgr = StartupManager()
        definitions = sMgr.getStartupDefinitions()
        length = len(definitions)
        print length
        sMgr = StartupManager()
        result = sMgr.remove_definition(1)
        self.assertTrue('code' in result)
        definitions = sMgr.getStartupDefinitions()
        print len(definitions)
        self.assertTrue(length == len(definitions) + 1)
        
if __name__ == '__main__':
    unittest.main()
