#!/usr/bin/python
import sys
import os
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/toolkit')
sys.path.append(os.environ['MY_HOME']+'/etc/config')
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/chrome')
from cern_vm import Configuration
from Adapter import GenericAdapter
from view import View

ID='System Information'

def main():
    '''
    Deprecated. Replaced by the generic module
    main.py
    which gets the ID from url and executes the adapter
    after reading from the xml configuration files
    '''
    config=Configuration()

    view = View(config.system.actions)
    action=config.system.actions[ID]

    adapter=GenericAdapter(ID, view, action.command_group)
    adapter.page()
    
if __name__ == '__main__':    
    main()
