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
sys.path.append(os.environ['MY_HOME']+'/cgi-bin')
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/chrome')
sys.path.append(os.environ['MY_HOME']+'/etc/config')
from framework import output, view, get_template
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
    mpm = MediaPlayerManager()
    if (not mpm.check_status()):
        view.setContent('Media Player', mpm._generateMissingDependenciesView())
        output(view,fs)
        return
    content = get_view()
    view.setContent('Mplayer', content)
    
    output(view, fs)
    
if __name__ == '__main__':    
    main()

