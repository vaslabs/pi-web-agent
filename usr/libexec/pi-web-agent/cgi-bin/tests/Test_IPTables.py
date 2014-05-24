import unittest
import sys
sys.path.append("../toolkit")
sys.path.append("..")
from add_iptable_rules import validate_address

class TestHTMLPageGenerator(unittest.TestCase):

    def test_update(self):
        self.assertTrue(None == validate_address("192; sudo reboot"));
        self.assertTrue (None == validate_address("192'; sudo reboot"));
        self.assertTrue(None == validate_address("192\"; sudo reboot"));
        self.assertTrue(validate_address("192.168.1.10") != None);
        self.assertTrue(validate_address("kemal.sunucuservis.com.tr") != None); 
        

if __name__ == '__main__':
    unittest.main()
