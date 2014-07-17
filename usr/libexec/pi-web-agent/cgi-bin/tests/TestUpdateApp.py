import sys, os
import unittest
import PiWebAgentTestSuite
class TestUpdateApp(unittest.TestCase):
    
    def test_update_check_script(self):
        import update_check
        self.assertTrue(update_check.check() != None)
        update_json = update_check.getNewUpdate()
        if ('code' in update_json):
            self.assertTrue(['code'] == 0)
        else:
            self.assertTrue('body' in update_check.getNewUpdate())
        
if __name__ == '__main__':
    unittest.main()
