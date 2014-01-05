import os, sys
sys.path.append(os.environ['MY_HOME']+'/etc/config')
from cern_vm import VERSION
def initialiseCss():
    with open(os.environ['MY_HOME']+'/html/utilities/blueprint-css.html', 'r') as content_file:
        content = content_file.read()
    return content
    
def createList(items, span):
    div='<div class="span'+str(span)+'">\n'
    div+='<div class="notice">'
    for item in items:
        div+=str(item)+'<hr>\n'
    div+='</div>\n</div>\n'
    return div
    
def createMenuList(items, span):
    if span == None:
        div="<div>"
    else:
        div='<div class="span'+str(span)+'">\n'
    div+='<div class="well">'
    
    div+='<ul class="nav nav-list">'
    div+='<li class="nav-header">Actions</li>'
    for item in items:
        div+=str(item) + '\n'
        div+='<li class="divider"></li>\n'
    div+='</ul></div>\n</div>\n'
    return div

def createNavList(items):

    div='<div class="container">\n<div class="navbar navbar-default navbar-fixed-bottom">\n<center>'
    div+='<ul class="nav nav-pills">\n'
    item_name='Home'
    item_actionlink='/'
    div+='<li><a href="' + item_actionlink + '">' + item_name + '</a></li>\n'
    for item in items:
        div+=str(item) + '\n'
        
    div+='</ul>\n</center>'
    div+='</div></div>\n'
    return div
        
def createNavListWithDropdown(items):

    div='<div class="container">\n<div id="awesome-navbar" class="navbar navbar-default">\n<center>'
    div+='<ul class="nav nav-pills">\n'
    item_name='Home'
    item_actionlink='/'
    div+='<li><a href="' + item_actionlink + '">' + item_name + '</a></li>\n'
    item_counter=1;
    MENU_LIMIT = 5
    for item in items:
        if item_counter < 5:
            div+=str(item) + '\n'
            item_counter+=1
        else:
            break
    div+='<li class="dropdown">\n<a href="#" class="dropdown-toggle" data-toggle="dropdown">Other<b class="caret"></b>\n</a>'
    div+='<ul class="dropdown-menu">\n'
    item_counter=1
    for item in items[len(items)-MENU_LIMIT + 1:len(items)]:
        div+=str(item) + '\n'
        item_counter+=1
        
    div+='</ul>\n'
    div+='</li>\n'
    div+='</ul>\n</center>'
    div+='</div></div>\n'
    return div

def createHeader(title, span, nav_bar):
    
    div='<header class="jumbotron subhead" id="overview">\n'
    div+='<div class="container">\n<div class="span24">'  
    div+='<h1><a href="/cgi-bin/index.py">'+\
    '<img src="/icons/logo.png" width="90" height="90" align="left">'+\
    title + '</a>'+\
     '<a href="http://www.icons-land.com">'+\
     '<img src="/icons/agent_logo.png" width="90" height="90" align="right">' +\
     '</a>' + '\n</h1>\n'
    div+='<p class="lead">Web-App Agent</p>\n'
    div+='</div>\n'
    
    div+='</div>\n'
    
    div+=nav_bar
    div+='\n</header>\n'
    
    return div
    
def createText(title, body, span):
    div='<div class="span'+str(span)+'">\n'
    div+='<h2>'+title+'</h2>\n'
    div+=body
    div+='\n</div>\n'    
    return div

def contain(divs):
    
    div='<div class="container">\n'
    for d in divs:
        div+=d+'\n'
    div+='</div>\n'
    return div
    
def createLegend(text):
    return "<legend>" + text + "</legend>\n"
    
def fieldset(action, method, name, widgets, legend=None):
    form = "<form"
    if len(name) > 0:
        form +=  " name=" + name    
    if len(action) > 0:
        form += " action=" + action
    if len(method) > 0:
        form +=  " method=" + method            
    form += ">\n"
    form+='<fieldset>\n'
    if (legend != None):
        form+=legend
    form+= widgets.toHtml() + "\n</fieldset>\n</form>"
    return form

def fieldsetTextarea(action, method, name, textarea, widgets, legend=None):
    form = "<form"
    if len(name) > 0:
        form +=  " name=" + name    
    if len(action) > 0:
        form += " action=" + action
    if len(method) > 0:
        form +=  " method=" + method            
    form += ">\n"
    form+='<fieldset>\n'
    if (legend != None):
        form+=legend
    form+=textarea
    form+= widgets.toHtml() + "\n</fieldset>\n</form>"
    return form
