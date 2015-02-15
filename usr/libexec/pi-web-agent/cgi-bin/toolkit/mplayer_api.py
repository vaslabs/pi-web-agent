#!/usr/bin/python
import cgi
import cgitb
import os
cgitb.enable()
import sys
import subprocess
import json
import httplib
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/chrome')
if 'ssl_cert' not in os.environ:
    os.environ['ssl_cert']='/etc/pi-web-agent/conf.d/certs/pi-web-agent.crt'
if 'ssl_key' not in os.environ:
    os.environ['ssl_key']='/etc/pi-web-agent/conf.d/certs/pi-web-agent.key'
from live_info import execute
from view import composeJS
__author__ = 'andreas'
__date__ = '$Sep 14, 2014 9:23:40 PM$'




# fire and forget success will be determined by triggering strace on websocket
# connection if strace fails web socket connection will fail .

def fireAndForget(command):
    subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

class SettingsReader(object):
    def __init__(self, fileURL):
        self.fileURL = fileURL

    def read(self):
        fp = open(self.fileURL)
        for (i, line) in enumerate(fp):
            if i == 0:
                self.volume = line
            elif i == 1:
                self.eq = line
            elif i > 1:
                break
        fp.close()

    def setURL(self, fileURL):
        self.fileURL = fileURL

    def getVolume(self):
        return self.volume

    def getEQ(self):
        return self.eq


#def execute(command):
#    sp = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
#    (output, err) = sp.communicate()
#    sp.wait()
#    return sp.returncode


class MPlayer:

    def __init__(
        self,
        uri,
        volume,
        output,
        ):

        self.uri = uri.strip()
        self.volume = volume

        # wow I ll be a bit pythonic here xD

        self.output = ('2' if output == 'HDMI' else ('1' if output
                       == 'HEADPHONES' else '0'))

    def startStream(self):
        '''
        try to use mplayer for the given parameters
        '''
        command=(os.environ['MY_HOME'] + "/scripts/mplayer.sh "+self.output+" "+str(self.volume)+" \""+self.uri + "\" "+os.environ['ssl_cert']+" "+os.environ['ssl_key']);
        fireAndForget(command)
        execute("echo '"+str(self.volume)+"\n0:0:0:0:0:0:0:0:0:0' > /tmp/mplayer_status")
        return 0;

if __name__ == '__main__':
    if os.environ['REQUEST_METHOD'] == 'GET':
        
        if execute('pidof mplayer')[1] == 0:
            fireAndForget('echo "get_property volume" > /tmp/mplayer-control;');
            composeJSON('{ "status" : "playing" }')
        else:
            composeJSON('{ "status" : "stoped" }')
    elif os.environ['REQUEST_METHOD'] == 'DELETE':

        if execute('echo "quit" > /tmp/mplayer-control')[1] == 0:
            composeJSON('{ "status" : "success" }')
        else:
            composeJSON('{ "status" : "failure" }',
                      httplib.INTERNAL_SERVER_ERROR)
    elif os.environ['REQUEST_METHOD'] == 'POST':
        data=json.loads(sys.stdin.read())
        try:
            if 'volume' in data:
                if 0 <= int(data['volume']) <= 100:
                    execute('echo "set_property volume '
                            + str(data['volume'])
                            + '" > /tmp/mplayer-control;echo "get_property volume" > /tmp/mplayer-control;')
                    
                    streqhelper = ':'.join(map(str, data['eqhelper']))
                    execute("echo '" + str(data['volume']) + '\n'
                            + streqhelper + "' > /tmp/mplayer_status")
                    composeJSON('{ "status" : "volume '
                              + str(data['volume']) + '" }')
                else:
                    composeJSON('{ "status" : "Oups!Invalid volume range.'
                               + 'Don\'t send castom requests!" }')
            elif 'eq' in data:
                c = 0
                for n in data['eq']:
                    if -12 <= n <= 12:
                        c += 1
                if c == 10:
                    streq = ':'.join(map(str, data['eq']))
                    execute('echo "af_cmdline equalizer ' + streq
                            + '" > /tmp/mplayer-control')
                    execute("echo '" + str(data['volumehelper']) + '\n'
                            + streq + "' > /tmp/mplayer_status")
                    composeJSON('{ "status" : "eq ' + streq + '" }')
                else:
                    streq = ':'.join(map(str, data['eq']))
                    composeJSON('{ "status" : "Invalid eq settings[-12/12]:'
                               + streq + '" }')
            elif 'init' in data and 'uri' in data['init']:
                if 'volume' in data['init'] and 0 <= int(data['init']['volume']) <= 100:
                    volume = data['init']['volume']
                else:
                    volume = 99
                if 'output' in data['init']:
                    output = data['init']['output']
                else:
                    output = 'HEADPHONES'
                if 'uri' in data['init']:
                    uri = data['init']['uri']
                else:
                    composeJSON('{ "status" : "failure" }')
                if execute('pidof mplayer')[1] != 0:
                    player = MPlayer(uri, volume, output)
                    if player.startStream()==0:
                        composeJSON('{ "status" : "starting" }')
                    else:
                        composeJSON('{ "status" : "failure" }')  
        except ValueError:

            composeJSON('{ "status" : "Invalid Input!Don\'t send custom'
                      + ' requests!" }')
    else:
        composeJSON('{ "status" : "unknown operation" }')