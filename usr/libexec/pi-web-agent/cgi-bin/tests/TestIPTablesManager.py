#!/usr/bin/python
import sys
import unittest
import os
import PiWebAgentTestSuite
from pi_iptables import IPTablesManager

def main():
	iptmgr = IPTablesManager()
	print str(iptmgr)	

if __name__=="__main__":
    main()
