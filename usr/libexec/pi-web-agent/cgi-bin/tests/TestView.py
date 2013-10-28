#!/usr/bin/python
import sys
sys.path.append('../chrome')
sys.path.append('..')
sys.path.append('../config') 
#replace sys.path.append by reading a configuration file
#with full paths
from menu import *
from view import View
from cern_vm import Configuration

def main():
    config = Configuration()
    indexView=View(config.system.actions)
    print indexView

main()
    
