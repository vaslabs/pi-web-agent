#!/usr/bin/python
import sys

sys.path.append('/etc/cernvm-applicance-agent/config')
from cern_vm import Configuration
sys.path.append(cern_vm.APP_PATH + '/cgi-bin/chrome')
sys.path.append(cern_vm.APP_PATH + '/cgi-bin/toolkit')
from Adapter import GenericAdapter
from view import View

def main():
    config=Configuration()
    view = View(config.system.actions)
    commands={'Host Name':'uname -n','Kernel' : 'uname -sr'}
    adapter=GenericAdapter('System Information', view, commands)
    adapter.output()
main()
