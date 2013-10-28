import os
import Adapter
from Adapter import *
import sys
sys.path.append(os.environ['MY_HOME']+'/cgi-bin')
import HTMLPageGenerator
from HTMLPageGenerator import *
#deprecated

UPDATE_OK = "System is updated"
UPDATE = "There are updates available for the system"
UPDATE_ERROR = "An error occured during update check"    
STATUS_OK = 0
STATUS_UPDATE = 100
STATUS_ERROR = 1

class UpdateAdapter(Adapter):
    
    

    def __init__(self):
        Adapter.__init__(self)        
        self.status={}
        self.status[STATUS_OK]=UPDATE_OK
        self.status[STATUS_ERROR]=UPDATE_ERROR
        self.status[STATUS_UPDATE]=UPDATE
        self.check()

    def check(self):
        fo = open("../update_file", "r")
        self.status_code=int(fo.read(1))
        fo.close()


    def message(self):
        try:
            return self.status[self.status_code]
        except:
            return "Uknown exit code."

    def command(self):
        iwg = InputWidgetGroup()
        iwg.addInputWidget(InputWidget('submit', 'update','Update',''))
        return iwg    
    

    def generateHtmlView(self):
        formArea = createForm('','','',self.command())
        msg = self.message()
        partition="<p>" + formArea + "<br> Exit code: " + str(self.status_code) + "<br>" + msg + "</p>"
        return createDiv(partition)
