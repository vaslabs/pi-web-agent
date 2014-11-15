# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import unittest
from mplayer_api import *
import time
class  Mplayer_apiTestCase(unittest.TestCase):
    #def setUp(self):
    #    self.foo = Mplayer_api()
    #

    #def tearDown(self):
    #    self.foo.dispose()
    #    self.foo = None

    def test_mplayer_api(self):
        player = MPlayer("http://imagine.1stepstream.com:8000/aac ", 50, "AUTO")
        player.startStream()
        time.sleep( 5 )
        self.assertEqual(0, execute('pidof mplayer')[1], "Msg");

        self.fail("test failed")

if __name__ == '__main__':
    unittest.main()

