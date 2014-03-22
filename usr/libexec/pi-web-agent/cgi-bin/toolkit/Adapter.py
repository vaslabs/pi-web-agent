import subprocess
import sys
import os
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME']+'/cgi-bin')
from HTMLPageGenerator import *
from BlueprintDesigner import *
import string
import cgi

def cleanUpStringList(strList):
    i=0
    while i < len(strList):
        if len(strList[i]) == 0:
            del strList[i]
        else:
            i+=1

class Adapter(object):
    '''
    Interface for building an adapter responsible
    for converting POSIX output from bash commands into
    html.
    '''
    def __init__(self, title, view):
        self.title=title
        self.subpages=[]
        self.view=view

    def message(self):
        self.addSubpage({"None":"Empty"})
    
    def command(self):
        return "None"
    
    def _page(self):
        return "Empty"

    def addSubpage(self, elements, title=None):
        return "Empty"
        
class GenericAdapter(Adapter):
    '''
    The GenericAdapter is responsible to convert
    simple output in table or raw style to html.
    '''
    #commands={title:command}    
    def __init__(self, title, view, commandgroup):
        Adapter.__init__(self, title, view)
        self.commandgroup = commandgroup
        
    def _message(self, commands):
        messageElements={}
        for command in commands:
            sp=subprocess.Popen(command.value, stdout=subprocess.PIPE, shell=True)
            output, _ = sp.communicate()
            sp.wait()
            normalised_output=output.split('\n')
            if command.format=='table':
                final_output=self._toTable(normalised_output)
            else:
                final_output=normalised_output[0]+'<br>'+normalised_output[1]
            messageElements[command.title]=final_output
        return messageElements

    def page(self):
        '''
        Page executes _message and gets the elements from 
        the commands of a command group. The _subpage gets the
        results of that set of commands (called command-group).
        Then each command group is converted to a subpage and the
        subpages shape the html of the main page.
        '''
        html=''
        for commandIDs in self.commandgroup:
            elements=self._message(self.commandgroup[commandIDs])
            self._subpage(elements)
        for subpage in self.subpages:
            html+=subpage+'<hr>'
        self.view.setContent(self.title, html)
        self.view.js_output()
        
    def _subpage(self, elements, title=None):
        html=''
        html+='<div class="info">'
        for element in elements:
            html+='<h3>'+element+': ' + '</h3>' + elements[element] + '<br><br>\n'
        html+='\n</div>'
        self.subpages.append(html)


    #rules to create a correct table:
    #every headline starts with a capital
    #all other words start with a lower
    #if a row has a string with spaces
    #this function is not the appropriate one 
    #to use.
    def _toTable(self, lines):
        div=False
        if len(lines)>10:
            html='<div class="limit">\n'
            div=True
        else:
            html=''
        html+='<table>\n<tr>\n'
        cleanUpStringList(lines)
        
        headlines=lines[0].split(' ')
        
        cleanUpStringList(headlines)
        i=0
        while i < len(headlines):
            
            if headlines[i][0] in string.ascii_uppercase:
                if i>0:
                    html+='</th>\n<th>'
                else:
                    html+='<th>'
                
            else:
                headlines[i-1]=' ' + headlines[i] #bit of a hack
                del headlines[i]
                i-=1

            html+=headlines[i]
            i+=1
        html+='</th></tr>'

        for i in range(1, len(lines)):
            html+='<tr>\n'
            cells=lines[i].split(' ')
            cleanUpStringList(cells)

            for j in range(0, len(cells)):
                html+='<td>' + cells[j]
                html+='</td>'          
            html+='</tr>\n'
        html+='\n</table>'
        if div:
            html+='\n</div>'    
        return html
        
                
    
    def _command(self):
        '''
        Creates a form widget with a button. Unused and not yet deployed,
        it should also get a list of input widgets to support more complicated
        functonality
        '''
        name=self.scriptpath.split('/')[-1]
        iw=InputWidget('submit', self.title, name.split('.')[0],'')
        iwg=InputWidgetGroup()
        iwg.add(iw)
        return createForm('/cgi-bin/toolkit/controller.py', 'POST', 'standard', iw)
         


class UserGenericAdapter(GenericAdapter):
    #unused and untested
    '''
    Does nothing yet
    '''
    def command(self):
        name=self.scriptpath.split('/')[-1]
        iw=InputWidget('submit',self.title, name.split('.')[0],'')
        iwg=InputWidgetGroup()
        iwg.add(iw)
        return createForm('userdefined/controller.py', 'POST', 'userdefined', iw)
        

        
