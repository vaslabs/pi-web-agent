#!/usr/bin/python
import sys
import unittest
import os
sys.path.append('/home/rpi/pi-web-agent/usr/share/api')
from pi_iptables import IPTablesManager

def main():
	iptmgr = IPTablesManager()
	print str(iptmgr)	

main()
