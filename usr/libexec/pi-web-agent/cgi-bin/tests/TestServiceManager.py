#!/usr/bin/python
import sys
sys.path.append(os.environ['CVM_AA_APP_PATH'] + '/cgi-bin')
sys.path.append(os.environ['CVM_AA_APP_PATH'] + '/toolkit')
sys.path.append(os.environ['CVM_AA_APP_PATH'] + '/chrome')
sys.path.append(os.environ['CVM_AA_CONFIG_PATH'])
from services import *
from view import *
from cern_vm import Configuration
def main():
    sm=serviceManagerBuilder()
    content=sm.getView()
    config=Configuration()
    view = View(config.system.actions)
    
    view.setContent('User Management App', content)
    view.output()

main()
    
