#!/usr/bin/python
import json
import urllib2

import sys, os
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME'] + '/etc/config')

from cern_vm import VERSION

LINK="https://api.github.com/repos/vaslabs/pi-web-agent/releases"
def getJSON():
	global LINK
	json_document = urllib2.urlopen(LINK)
	json_text = json_document.read()
	json_struct = json.loads(json_text)	
	
	return json_struct[0]


def readTagFromRemote(json_struct):
	return json_struct['tag_name']

FILE="etc/pi-web-agent/tag"

def readCurrentTag():
	return VERSION





