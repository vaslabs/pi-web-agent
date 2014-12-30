import os, sys
sys.path.append(os.environ['MY_HOME']+'/etc/config')

def createText(title, body, span=None):
    if (span == None):
        div=""
    else:
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
def customFieldset(action, method, name, html, legend=None):
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
    form+= html + "\n</fieldset>\n</form>"
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
