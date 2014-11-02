#!/usr/bin/python
# -*- coding: utf-8 -*-
# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import cgi
import cgitb
import os
cgitb.enable()
import sys
import subprocess
import json
import httplib
__author__ = 'andreas'
__date__ = '$Sep 14, 2014 9:23:40 PM$'


# codes from https://docs.python.org/3.0/library/httplib.html

def jsonReply(stringifiedJSON, code=httplib.OK):
    print 'Status: ', code, ' ', httplib.responses[code]
    print 'Content-Type: application/json'
    print 'Cache-Control: no-store'
    print 'Length:', len(stringifiedJSON)
    print ''
    print stringifiedJSON


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

def execute(command):
	sp=subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
	output, err = sp.communicate()
	sp.wait()
	return sp.returncode
class MPlayer:

    def __init__(
        self,
        uri,
        volume,
        output,
        ):
        self.uri = uri
        self.volume = volume
        self.output = output

    def startStream(self):
        '''
        try to use mplayer for the given parameters
        '''

        self.uri = urllib.unquote(self.uri).decode('utf8')

        # wow I ll be a bit pythonic here xD

        self.outout = ('2' if self.form.getvalue('output') == 'HDMI'
                        else ('1' if self.form.getvalue('output')
                       == 'HEADPHONES' else '0'))
        command = \
            "sh -c '[ -f /tmp/mplayer-control ]|| mkfifo /tmp/mplayer-control;sudo amixer cset numid=3 " \
            + self.outout \
            + ';sudo mplayer -slave -input file=/tmp/mplayer-control -ao alsa:device=hw -af equalizer=0:0:0:0:0:0:0:0:0:0 '

        command += ' -volume ' + self.volume
        command += ' "' + self.uri + '" </dev/null >/dev/null 2>&1 &\''
        fireAndForget(command)
        execute("echo '" + self.volume
                + "\n0:0:0:0:0:0:0:0:0:0' > /tmp/mplayer_status")


if __name__ == '__main__':
    if os.environ['REQUEST_METHOD'] == 'GET':
        if execute('pidof mplayer') == 0:
            jsonReply('{ "status" : "playing" }')
        else:
            jsonReply('{ "status" : "stoped" }')
    elif os.environ['REQUEST_METHOD'] == 'DELETE':

        if execute('echo "quit" > /tmp/mplayer-control') == 0:
            jsonReply('{ "status" : "success" }')
        else:
            jsonReply('{ "status" : "failure" }',
                      httplib.INTERNAL_SERVER_ERROR)
    elif os.environ['REQUEST_METHOD'] == 'POST':
        data = json.loads(sys.stdin.read())
        try:
            if 'volume' in data:
                if 0 <= int(data['volume']) <= 100:
                    execute('echo "set_property volume '
                            + str(data['volume'])
                            + '" > /tmp/mplayer-control')
                    streqhelper = ':'.join(map(str, data['eqhelper']))
                    execute("echo '" + str(data['volume']) + '\n'
                            + streqhelper + "' > /tmp/mplayer_status")
                    jsonReply('{ "status" : "volume '
                              + str(data['volume']) + '" }')
                else:
                    jsonReply('{ "status" : "Oups!In valid volume range.'
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
                    jsonReply('{ "status" : "eq ' + streq + '" }')
                else:
                    streq = ':'.join(map(str, data['eq']))
                    jsonReply('{ "status" : "Invalid eq settings[-12/12]:'
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
                    sys.exit()
                if execute('pidof mplayer') == 0:
                    player = MPlayer(uri, volume, output)
                    player.startStream()
                    jsonReply('{ "status" : "starting" }')
        except ValueError:
            jsonReply('{ "status" : "Invalid Input!Don\'t send custom'
                      + ' requests!" }')
    else:
        jsonReply('{ "status" : "unknown operation" }')