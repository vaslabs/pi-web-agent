#!/usr/bin/python
import sys
import os
import cgi
import cgitb

cgitb.enable()
sys.path.append(os.environ['MY_HOME']+'/cgi-bin')
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/chrome')
sys.path.append(os.environ['MY_HOME']+'/etc/config')
from HTMLPageGenerator import *
from BlueprintDesigner import *
from view import *
from cern_vm import Configuration
class TextEditor():

    def __init__(self):
        self.message="Initialised" 

def getView():
    
    textarea=createTextArea('Write your code here', tClass=None, attribs='id="text_editor" style="height: 250px; width: 100%;"')
    iw_submit=InputWidget('submit', '', 'Save Text', '', wClass='btn btn-warning')
    iwg = InputWidgetGroup()
    iwg.widgets=[iw_submit] 
    return fieldsetTextarea('', 'post', '', textarea, iwg, createLegend("Example 2"))

def main():
    te=TextEditor()
    fs=cgi.FieldStorage()
    config=Configuration()
    view=View(config.system.actions)
    
    content=getView()
    view.setContent('Text Editor', content)
    view.output()
    
if __name__ == '__main__':    
    main()
