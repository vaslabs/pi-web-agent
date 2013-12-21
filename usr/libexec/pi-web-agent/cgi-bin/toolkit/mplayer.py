#!/usr/bin/python
import cgi
import cgitb
import os
cgitb.enable()
import sys
sys.path.append(os.environ['MY_HOME']+'/scripts')
sys.path.append(os.environ['MY_HOME']+'/etc/config')
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/chrome')
sys.path.append(os.environ['MY_HOME'] + '/cgi-bin')
from HTMLPageGenerator import *
from BlueprintDesigner import *
from cern_vm import Configuration
import subprocess
from view import View
from urlparse import urlparse
def fireAndForget(command):
    subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
def execute(command):
    sp=subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = sp.communicate()
    sp.wait()
    return [output, sp.returncode]
def getView():
    iwpasswd = InputWidget('text', 'uri', '', 'URI: ',wClass='form-control ',
											attribs='placeholder="http ... or rtsp ..."')
    iwpasswd_new1=InputWidget('text', 'volume', '', 'Volume: ',
    						wClass='form-control ', attribs='placeholder="1 to 100"')
    iwpasswd_new2=InputWidget('text', 'cache', '', 'Cache: ',
    wClass='form-control',attribs='placeholder="0 to 99"')
    iw_submit=InputWidget('submit', '', 'Start Stream', '',
    																  wClass='btn btn-primary')
    iwg = InputWidgetGroup()
    iwg.widgets=[iwpasswd, iwpasswd_new1, iwpasswd_new2, iw_submit] 
    return fieldset('/cgi-bin/toolkit/mplayer.py', 'POST', 'stream_form', iwg,
    														 createLegend("Start Streaming"))
class MPlayer(object):

    
    def __init__(self, form):
        self.form = form
        
        
    def startStream(self):
        '''
    try to use mplayer for the given parameters
    '''
        self.uri=self.form.getvalue("uri")
        self.volume=self.form.getvalue("volume")
        self.cache=self.form.getvalue("cache") 
        command=("sh -c '[ -f /tmp/mplayer-control ]" 
                 "|| mkfifo /tmp/mplayer-control;"
                 " sudo mplayer -slave -input "
                 "file=/tmp/mplayer-control -ao alsa:device=hw "
                 "-af equalizer=0:0:0:0:0:0:0:0:0:0 -cache-min ") 
        command+=self.cache+" -volume "+self.volume+" "
        command+=self.uri+" </dev/null >/dev/null 2>&1 &'"
        fireAndForget(command)


def getRunningView():
    script='''
		<link rel="stylesheet" href="/css/jquery-ui.css">
		<script src="/css/jquery-ui.js"></script>
		<style>
			#eq span {
				height:120px; float:left; margin:15px
			}
		</style>
		<script src="/css/sliders.js"></script>
    	<script>
    
			var checkT;
         
			function checkStatus(){
				$.getJSON( "mplayer_status.py", function( data ) {
				if (data.redirect) {
					// data.redirect id the redirection link
            	location.href=data.redirect;
				}
				else {
					updateStatus(data)
             
				}});
            
				checkT=setTimeout(function() {checkStatus()},2000);
			}
			checkT=setTimeout(function() {checkStatus()},2000);
       
		</script>
		<p class="ui-state-default ui-corner-all ui-helper-clearfix" 
															style="padding:4px;">
			<span class="ui-icon ui-icon-volume-on" style="float:left;
			                             margin:-2px 5px 0 0;"></span>
			<span class="ui-icon ui-icon-signal" 
						style="float:left; margin:-2px 5px 0 0;"></span>
			Main controls and volume
		</p>
		<link rel="stylesheet" href="/css/toolbar.css">
		<script src="/css/player_controls.js"></script>
		<div id="toolbar" class="ui-widget-header ui-corner-all"
												style="margin-left:227.5px;">
		<!---needed in future release <button id="beginning">
														go to beginning</button>
		<button id="rewind">rewind</button>
		<button id="play">pause</button>--->
		<button id="stop">stop</button>
		<!---needed in future release 
		<button id="forward">fast forward</button>
		<button id="end">go to end</button>
		<input type="checkbox" id="shuffle"><label for="shuffle">Shuffle</label>
		<span id="repeat">
			<input type="radio" id="repeat0" name="repeat" checked="checked">
			<label for="repeat0">No Repeat</label>
			<input type="radio" id="repeat1" name="repeat">
			<label for="repeat1">Once</label>
			<input type="radio" id="repeatall" name="repeat">
			<label for="repeatall">All</label>--->
			<div id="master" style="width:260px; margin:15px;"></div>
		</span>         
       <div id="status">wait...</div></div>

		<p class="ui-state-default ui-corner-all" style="padding:4px;margin-top:4em;">
			<span class="ui-icon ui-icon-signal" 
												style="float:left; margin:-2px 5px 0 0;"></span>
			Graphic EQ
		</p>
		<div id="eq" style="margin-left:227.5px;">
			<span>0</span>
			<span>0</span>
			<span>0</span>
			<span>0</span>
			<span>0</span>
			<span>0</span>
			<span>0</span>
			<span>0</span>
			<span>0</span>
			<span>0</span>
		</div>
 
         '''

    return script
def main():
    """
    The mplayer port for py web agent
    If you read this code, it is better acompanied
    with the following documentation for improved
    understanding:
    http://www.mplayerhq.hu/DOCS/man/en/mplayer.1.txt 
    You can also have a look at:
    http://jqueryui.com/slider/ for /css/sliders.js
    And for mplayer_status.py:
    	mplayer slave cmmands:
    		http://www.mplayerhq.hu/DOCS/tech/slave.txt
    	rfc3875:
    		http://www.ietf.org/rfc/rfc3875.txt
    If you have any questons abou this feature send me an email at:
    andreasgalazis-AT-yahoo.com(replace -At- with @)
    or for more generic pi-web agent questions
    ask any member of the kupepia team.
    """
    form = cgi.FieldStorage()
    config=Configuration()
    view = View(config.system.actions) 
    if (execute('pidof mplayer')[1]==0):
        view.setContent('Mplayer', getRunningView())
    elif "uri" not in form and "volume" not in form and "cache" not in form:
        view.setContent('Mplayer', getView())
    else:
        player = MPlayer(form)
        player.startStream();
        view.setContent('Mplayer', getRunningView())
    view.output()







if __name__ == '__main__':
    main()    
    
