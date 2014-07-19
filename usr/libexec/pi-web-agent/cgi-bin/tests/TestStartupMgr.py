import sys, os
import unittest
import PiWebAgentTestSuite
class TestStartupMgr(unittest.TestCase):
    
    def test_set_startup_defs(self):
        from startup_manager import StartupManager
        sMgr = StartupManager()
        result = sMgr.setStartupDefinition('python', '')
        self.assertTrue(result['code'] == 0)
        result = sMgr.setStartupDefinition('true', '')
        self.assertTrue(result['code'] == 0)
        
    def test_api_syntax(self):
        import startup_manager_api
        
if __name__ == '__main__':
    unittest.main()
