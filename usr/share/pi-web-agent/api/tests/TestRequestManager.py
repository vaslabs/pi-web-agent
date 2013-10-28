import sys
sys.path.append('../api-bin')
import unittest
from pi_api import *
import xml.etree.ElementTree as ET
import urllib
import urllib2
def post(transaction):
    xml_string = ET.tostring(transaction, encoding='UTF-8')
    data = urllib.urlencode({'xml': xml_string})
    url='https://127.0.0.1:8005/api-bin/pi_api.py'
    response = urllib2.urlopen(url, data)
    for line in response.readlines():
        print line

class TestRequestManager(unittest.TestCase):

    def test_authentication(self):
        el_request = ET.Element('request', {'type':'authentication'})
        el_username = ET.Element('username')
        el_username.text='admin'
        el_apikey = ET.Element('api-key')
        el_apikey.text = "17g5HwTpKfVjM"
        el_request.append(el_username)
        el_request.append(el_apikey)
        el_tree = ET.ElementTree()
        el_tree._setroot(el_request)
        rm = RequestManager(el_tree)
        rm.submit()
        
    def test_post(self):
        el_request = ET.Element('request', {'type':'authentication'})
        el_username = ET.Element('username')
        el_username.text='admin'
        el_apikey = ET.Element('api-key')
        el_apikey.text = "17g5HwTpKfVjM"
        el_request.append(el_username)
        el_request.append(el_apikey)
        post(el_request)    


if __name__ == '__main__':
    unittest.main()
