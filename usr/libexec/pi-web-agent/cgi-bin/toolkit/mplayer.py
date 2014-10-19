#!/usr/bin/python
# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="andreas"
__date__ ="$Sep 14, 2014 10:56:15 AM$"
import sys
import os
import cgi
import cgitb

cgitb.enable()
#debug line os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME']+'/cgi-bin')
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/chrome')
sys.path.append(os.environ['MY_HOME']+'/etc/config')
from framework import output, view, get_template
from BlueprintDesigner import *
from HTMLPageGenerator import *
from DependableExtension import DependableExtension
class MediaPlayerManager(DependableExtension):
    def __init__(self):
        DependableExtension.__init__(self, EXTENSION_ID)
    
def get_view():
    try:
        with open(get_template("mplayer")) as template:
            return template.read()
    except:
        return "<p>Unexpected error:"+ sys.exc_info()[0]+"</p>"
        

def main():
    # Serves the mplayer page
    fs = cgi.FieldStorage()
    content = get_view()
    view.setContent('Mplayer', content)
    
    output(view, fs)
    
if __name__ == '__main__':    
    main()

