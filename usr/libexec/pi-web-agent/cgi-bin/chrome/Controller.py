import sys
import os
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/toolkit')
import UpdateAdapter
from UpdateAdapter import *
class Controller(object):

    #deprecated
    def __init__(self):
        self.name="Controller"
        self.updater=None
    
    def getUpdateView(self):
        if self.updater == None:
            self.updater = UpdateAdapter()
        return self.updater.generateHtmlView()                         
