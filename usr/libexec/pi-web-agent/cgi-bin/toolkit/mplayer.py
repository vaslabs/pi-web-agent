#!/usr/bin/python
import cgi
import cgitb
import os
cgitb.enable()
import sys
sys.path.append(os.environ['MY_HOME']+'/objects')
sys.path.append(os.environ['MY_HOME']+'/etc/config')
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/chrome')
sys.path.append(os.environ['MY_HOME'] + '/cgi-bin')
from HTMLPageGenerator import *
from BlueprintDesigner import *
from cern_vm import Configuration
import subprocess
from view import View
from urlparse import urlparse
from live_info import execute
from framework import output

def fireAndForget(command):
    subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
def getView(err):
    uri = InputWidget('text', 'uri', '', 'URI: ',wClass='form-control ',
											attribs='placeholder="http ... or rtsp ..."')									
    slider='''
    		<link rel="stylesheet" href="/css/jquery-ui.css">
		<script src="/css/jquery-ui.js"></script>
    
    <div id="slider"></div>
    	Volume:
		<input type="text" name="volume" id="volume" style="border:0; color:#f6931f; font-weight:bold;" readonly />
		<script>
	 	$sliderValue="";
		$("#slider").slider({                   
                value: 50,
                min: 0,
                max: 99,
                step: 1,
                slide: function(event, ui) {
                                $("#volume").val(ui.value);
                          },
            stop: function(event, ui) {
                $sliderValue=ui.value;
            }
        });
        $("#volume").val($("#slider").slider("value"));
        </script>'''
	 
    radioButtons='''
  	 	<div id="radio">
    	<input type="radio" id="hdmi" name="selection"><label for="hdmi">HDMI</label>
    	<input type="radio" id="auto" name="selection" checked="checked"><label for="auto">AUTO</label>
    	<input type="radio" id="headphones" name="selection"><label for="headphones">HEADPHONES</label>
    	
  	 	</div>
  	 	<input type="hidden" name="output" value="AUTO">
  	 	<script>
  	 	$(function() {
     		$( "#radio" ).buttonset();
    		$("#radio label").click(function(){
     			$("[name=output]").val($(this).text());
     			
     		});
  	 	});
    	</script>'''
    if err :
    	alert ='<div class="error">'+err+'</div>' ;  
    else:
    	alert="";
    iw_submit=InputWidget('submit', '', 'Start Stream', '',
    																  wClass='btn btn-primary')
    return customFieldset('/cgi-bin/toolkit/mplayer.py', 'POST', 'stream_form',alert+uri.toHtml()+slider+iw_submit.toHtml()+radioButtons,
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
        #wow I ll be a bit pythonic here xD
        self.outout="2" if self.form.getvalue("output")=="HDMI" else "1" if self.form.getvalue("output")=="HEADPHONES" else "0"
        command=("sh -c '[ -f /tmp/mplayer-control ]" 
                 "|| mkfifo /tmp/mplayer-control;"
                 "sudo amixer cset numid=3 "+self.outout+";"
                 "sudo mplayer -slave -input "
                 "file=/tmp/mplayer-control -ao alsa:device=hw "
                 "-af equalizer=0:0:0:0:0:0:0:0:0:0 ") 
        command+=" -volume "+self.volume+" "
        command+=self.uri+" </dev/null >/dev/null 2>&1 &'"
        fireAndForget(command)
        execute("echo '"+self.volume+"\n0:0:0:0:0:0:0:0:0:0' > /tmp/mplayer_status")
class SettingsReader(object):
    def __init__(self, fileURL):
        self.fileURL = fileURL
    def read(self):
        fp = open(self.fileURL)
        for i, line in enumerate(fp):
    			if i == 0:
    				self.volume=line
    			elif i == 1:
    				self.eq=line
    			elif i > 1:
    				break
        fp.close()
    def setURL(self, fileURL):
        self.fileURL = fileURL
    def getVolume(self):
        return self.volume
    def getEQ(self):
        return self.eq	
		
def getRunningView(volume, eq):
    script='''
		<link rel="stylesheet" href="/css/jquery-ui.css">
		<script src="/css/jquery-ui.js"></script>
		<style>
			#eq span {
				height:120px; float:left; margin:15px
			}
		</style>
		
    	<script>
         window.volume= '''
    script+=volume         
    script+=''';
         window.eqvals=['''
    script+=",".join(eq)
    script+='''];    
			function checkStatus(){
				$.getJSON( "mplayer_status.py", function( data ) {
				if (data.redirect) {
					// data.redirect is the redirection link
            	location.href=data.redirect;
				}
				else {
					updateStatus(data)
             
				}});
            
				
			}
			window.setInterval(function(){checkStatus()},3000);
       
		</script>
		<script src="/css/sliders.js"></script>
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
		<div id="eq" style="margin-left:227.5px;"><span>'''
    script+="</span><span>".join(eq)
 
    script+=   '''
				</span>
		</div>'''
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
    If you have any questons about this feature send me an email at:
    andreasgalazis-AT-yahoo.com(replace -At- with @)
    or for more generic pi-web agent questions
    ask any member of the kupepia team.
    """
    form = cgi.FieldStorage()
    config=Configuration()
    view = View(config.system.actions) 
    if execute('pidof mplayer')[1]==0:
        settingsReader=SettingsReader("/tmp/mplayer_status")
        settingsReader.read()
        view.setContent('Mplayer', getRunningView(settingsReader.getVolume(), settingsReader.getEQ().split(':')))
    elif "uri" not in form and "volume" not in form:
        view.setContent('Radio', getView(None))
    elif "uri" not in form :
        view.setContent('Radio', getView("Please provide a uri"))
    else:
        player = MPlayer(form)
        player.startStream();
        view.setContent('Radio', getRunningView(form.getvalue("volume"),"0:0:0:0:0:0:0:0:0:0".split(':')))
    
    output(view, form)





if __name__ == '__main__':
    main()    
    
