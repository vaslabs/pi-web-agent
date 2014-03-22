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
	
	return json_struct[0] #get latest release


def readTagFromRemote(json_struct):
	return json_struct['tag_name']

FILE="etc/pi-web-agent/tag"

def readCurrentTag():
	return VERSION


def getParts(version):
    versionParts = version.split('.')
    major = versionParts[0]
    minor = versionParts[1]
    releaseCandidate = 0
    if '-' in minor:
        minor = minor.split('-')[0]
        releaseCandidate = version.split('-rc-')[1]
    
    return [major, minor, releaseCandidate]
    
    

def compareVersions(versionA, versionB):
    '''
    returns true if versionB is newer than A
    '''
    version_A_parts = getParts(versionA)
    version_B_parts = getParts(versionB)
    
    for i in range(0, 3):
        if version_B_parts[i] > version_A_parts[i]:
            return True
        elif version_B_parts[i] < version_A_parts[i]:
            return False
            
    return False 
    
        
def check(update_json=None):
    if update_json == None:
        return compareVersions(readCurrentTag(), readTagFromRemote(getJSON()))
    else:
        return compareVersions(readCurrentTag(), readTagFromRemote(update_json))
        
def getReleaseLink():

    repo_json = getJSON()
    if check(repo_json):
        return repo_json["zipball_url"]
    else:
        return ""
        
def main():
    print getReleaseLink()
    
if __name__ == "__main__":
    main()
