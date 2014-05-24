#!/usr/bin/python
import sys, os
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/api')
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/')
sys.path.append(os.environ['MY_HOME'] + '/etc/config')


import cgi
import cgitb
from subprocess import Popen, PIPE
import json
cgitb.enable()

from live_info import execute
import re

def validate_address(ip):
    regex = re.compile(
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return regex.match(ip)
           

#executes the command to add a new protocol rule
def addProtocolRule(chain, action, protocol):
    return execute('sudo iptables -A ' + chain + ' -p ' + protocol + ' -j ' + action)

def addIPRule(chain, action, ip_address):
    if (validate_address(ip_address) == None):
        return
    return execute('sudo iptables -A ' + chain + ' -s ' + ip_address + ' -j ' + action)

def addIPwithProtocolRule(chain, action, protocol, ip_address):
    if (validate_address(ip_address) == None):
        return
    return execute('sudo iptables -A ' + chain + ' -p ' + protocol + ' -s ' + ip_address + ' -j ' + action)

def main():   
    form = cgi.FieldStorage()
    chain = form['chain'].value
    protocol=form['protocol'].value
    action=form['action'].value
    ip_address=form['ipaddress'].value
    if protocol=="None":
        addIPRule(chain, action, ip_address)
    elif ip_address=="None":
        addProtocolRule(chain, action, protocol)
    else:
        addIPwithProtocolRule(chain, action, protocol, ip_address)
    response = {"code":0}
        
    composeJS(json.dumps(response))

if __name__ == '__main__':
    main()
