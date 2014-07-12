import sys
import os
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME']+'/cgi-bin')
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/chrome')
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/toolkit')
sys.path.append(os.environ['MY_HOME']+'/etc/config')
from BlueprintDesigner import *
from menu import *
from HTMLPageGenerator import *
import cgi
from pi_web_agent import VERSION
#any extension should be a subclass of view. View implements by default the default views
#of the menus in the user interface. The difference of each subclass of view should be
#on the content part of the interface. 

#The interface consists of two columns, one on the left and one on the far right. In the
#middle there are the results of an action and possible options and actions.


class View(object):
    '''
    This class forms the skeleton of the main view of the system. It forms
    the menus, titles and the main display area, where the results of each
    call are placed. This is returned by the function content. The rest are
    private since the skeleton parts must remain the same through the application's
    lifecycle
    '''

    def __init__(self, actions, cmdactions):
        self.menu=Menu([])
        self.nav_bar=Menu([], nav=True)
        self.actions=actions
        for action in actions:
            if not 'version' in actions[action]:
                version=""
            else:
                version = "<sup><sup>" + actions[action]['version'] + "</sup></sup>"
            self.nav_bar.addItem(MenuItem(actions[action]['title'] + version,\
                 actions[action]['url']))
        if cmdactions != None:    
            for cmdaction in cmdactions:
                 self.menu.addItem(MenuItem(cmdactions[cmdaction]['title'],\
                    cmdactions[cmdaction]['url']))
            
        self.title='The RPi'
        self.titlespan=24
        self.listspan=4
        self.contentspan=16
        self.setContent('Welcome', 'This is the web agent for the Raspberry PI')
        
    def setContent(self, title, content):
        """
        gets a title and a content in pure html and finilises the 
        shape and look of the user interface
        """
        self.contentTitle = title
        self.content = content
        self._view()    
    
    #def _titleView(self):
     #   return createTitle(self.title, self.titlespan)
        
    def _leftListView(self):
        with open(os.environ['MY_HOME']+"/html/utilities/information_list.html", "r") as listFile:
            data = listFile.read()    
        return data
    
    def _createNavBar(self):
        return str(self.nav_bar)    
        
    def _rightListView(self):
        with open(os.environ['MY_HOME']+"/html/utilities/facebook_page.html", "r") as fbpageFile:
            fbpage = fbpageFile.read()
        fbpageFile.close()
        rightSide = '<div class="span4 last">' +\
         createMenuList(self.menu.items, span=None) + "\n" + fbpage + '</div>'    
        return rightSide
    
    def _dialog(self):
        return "<div id='dialog' title='pi-web-agent'><span id='dialog_content'></span></div>"
    
    def _mainWindow(self):
        return createText(self.contentTitle, self.content + self._dialog(), self.contentspan)
    
    def _footer(self):
        return '<footer><center>\n'+\
        '<p><font size="2"> Version: ' + VERSION + '</font></p>' +\
        '<p><font size="2">Copyright &copy; Kupepia 2013</font><br>\n'+\
        '<img src=\'/icons/cy.png\' width="40" height="30"/><font size="1"> 100% Cyprus Product</font></p>\n'+\
        '<p><time pubdate datetime="26/10/2013"></time></p>\n'+\
        '</center></footer>' 
    
    def _view(self):
        self.mainhtml=createHeader(self.title, 16, self._createNavBar())+\
        contain([self._leftListView(),\
         self._mainWindow(), self._rightListView(), self._footer()])


    def output(self):
        '''
        Outputs the html in proper way to be 
        read from the browser, with the composeDocument
        function which is responsible to add the css declarations
        '''
        composeDocument(initialiseCss(), self.mainhtml + self._dialog())

    def js_output(self):
        composeJS(createText(self.contentTitle, self.content))
	

