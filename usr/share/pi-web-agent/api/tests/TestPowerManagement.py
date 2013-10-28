import sys
sys.path.append('../api-bin')
import unittest
from pi_api import *
import xml.etree.ElementTree as ET
import urllib
import urllib2
def post(transaction, url):
    xml_string = ET.tostring(transaction, encoding='UTF-8')
    data = urllib.urlencode({'xml': xml_string})
    response = urllib2.urlopen(url, data)
    for line in response.readlines():
        print line

class TestPowerManagement(unittest.TestCase):
        
    def test_post(self):
        el_request = ET.Element('request')
        el_authentication = ET.Element('authentication')
        el_username = ET.Element('username')
        el_username.text='admin'
        el_apikey = ET.Element('api-key')
        el_apikey.text='95AzDfIDImipA'
        el_pair = ET.Element('pair')
        el_key = ET.Element('key')
        el_key.text='def://power_management'
        el_value = ET.Element('value')
        el_value.text = "default"
        el_authentication.append(el_username)
        el_authentication.append(el_apikey)
        el_pair.append(el_key)
        el_pair.append(el_value)
        el_request.append(el_authentication)
        el_request.append(el_pair)
        url='https://127.0.0.1:8005/api-bin/power_management_android.py'
        post(el_request,url)    

if __name__ == '__main__':
    unittest.main()
