#!/usr/bin/python
import sys
import os
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME'] + '/cgi-bin')
sys.path.append(os.environ['MY_HOME'] + '/cgi-bin/chrome')
from BlueprintDesigner import *
from HTMLPageGenerator import *
from menu import *
#to be run on the browser
def main():
    listitems=Menu([])
    for i in range(0,15):
        listitems.addItem(MenuItem('Menu Item ' + str(i+1), 'http://www.google.co.uk'))
    title = 'Test of Blueprint designer'
    content='Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    contentTitle='Lorem ipsum'
    title_span=24
    leftlist=['Cern-VM']
    listspan=4
    content_span=16
    mainhtml=contain([createHeader(title, title_span, createList(leftlist,listspan), createText(contentTitle, content, content_span), str(listitems)])
    composeDocument(initialiseCss(), mainhtml)
    
main()
    
