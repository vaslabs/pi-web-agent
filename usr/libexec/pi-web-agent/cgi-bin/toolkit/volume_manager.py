#!/usr/bin/python
import sys
import os
import cgi
import cgitb

cgitb.enable()
sys.path.append(os.environ['MY_HOME']+'/cgi-bin')
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/chrome')
sys.path.append(os.environ['MY_HOME']+'/etc/config')
from framework import output, view
from BlueprintDesigner import *
from HTMLPageGenerator import *
from volume_controller import get_volume


def get_view():
    content =  '''
    <link rel="stylesheet" href="/css/jquery-ui.css">
    <script src="/css/jquery-ui.js"></script>
    <script src="/css/volume_manager.js" type="text/javascript"></script>
    
    <script src="/css/appDefinitions.js" type="text/javascript"></script>
    <link href="/css/openDialog.css" type="text/css" rel="stylesheet" />
    
    <p class="ui-state-default ui-corner-all ui-helper-clearfix" style="padding:4px;">
    <span class="ui-icon ui-icon-volume-on" style="float:left; margin:-2px 5px 0 0;"></span>
    Master
    </p>

    <p>
    <label for="amount">Volume:</label>
    <input type="text" id="amount" readonly style="border:0; color:#f6931f; font-weight:bold;">
    </p>
 
    <div id="slider-vertical" style="height:200px;"></div>

    Curent volume is: {vol}
    
    '''

    return content.format(vol=get_volume())
    
def main():
    fs = cgi.FieldStorage()
    content = get_view()
    view.setContent('Volume manager', content)
    
    output(view, fs)
    
if __name__ == '__main__':    
    main()
