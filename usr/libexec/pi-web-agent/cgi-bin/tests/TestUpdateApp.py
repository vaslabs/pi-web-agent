import sys, os
import unittest
import PiWebAgentTestSuite
class TestUpdateApp(unittest.TestCase):
    
    def test_update_check_script(self):
        import update_check
        self.assertTrue(update_check.check() != None)
        
if __name__ == '__main__':
    unittest.main()
