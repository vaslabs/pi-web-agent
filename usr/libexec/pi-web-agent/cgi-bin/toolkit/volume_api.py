#!/usr/bin/python
import json
import os, sys
from live_info import execute
import cgi, cgitb
cgitb.enable()
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME'] + '/etc/config')

from HTMLPageGenerator import composeJS
from framework import view, output
from functools import partial
import re

status={'on':True, 'off':False}

def get_volume(args):
    # Returns current volume of args['mixer']
    command = "sudo amixer sget {mixer}"
    out, exit_code = execute(command.format(mixer=args['mixer']))
    m = re.search("[0-9]+%", out)
    vol = m.group(0)[:-1]
    data_line = out.split('\n')[-2]
    m = re.search("(\[on\]|\[off\])+", data_line)
    st = m.group(0)
    return json.dumps({'volume':int(vol), 'status':status[st[1:-1]]})

def set_volume(args):
    # Sets volume of mixer specified in args
    command = "sudo amixer sset {mixer} {vol}\%"
    out, exit_code = execute(command.format(mixer=args['mixer'],
                                            vol=args['val']))

    return json.dumps(args)
    
def get_mixers(args):
    out, exit_code = execute("sudo amixer scontrols")
    mixers = re.findall(r"'.+'", out)
    mixers = list(m[1:-1] for m in mixers)

    return json.dumps(mixers)

def error():
    return json.dumps("Error")

def toggle_mute(args):
    command = "sudo amixer sset {mixer} toggle"
    mixer = args['mixer']
    cmd = command.format(mixer=args['mixer'])
    out, exit_code = execute(cmd)
    return get_volume(args)

def test_speakers():
    execute('mplayer \'http://translate.google.com/translate_tts?tl=en&q="This is a sound test"\'')
    return json.dumps({'code':0})

def op_dispatch(form):
    op = form.getfirst("op")
    args = dict((k, form[k].value) for k in form.keys() if not k=="op")
    
    op_dict = {
        "get_vol"    : partial(get_volume, args=args),
        "update_vol" : partial(set_volume, args=args),
        "mixers"     : partial(get_mixers, args=args),
        "toggle"     : partial(toggle_mute, args=args),
        "test"       : test_speakers
    }

    op_func = op_dict.get(op, error)
    composeJS(op_func())
    
def main():
    # main entry point for the volume controller api
    # do a dispatch on the url command and call
    # the corresponding function
    #
    #
    # TODO: Fail gracefully
    form = cgi.FieldStorage()
    op_dispatch(form)
    
        
if __name__ == "__main__":
    main()
