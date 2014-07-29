#!/usr/bin/python
import sys, os
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/api')
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/')
from HTMLPageGenerator import *
from cernvm import Response
import cgi
import cgitb
cgitb.enable()
from live_info import execute

gpio="/usr/local/bin/gpio"

def set_pin_value(args):
    value = args['value']
    pin_no = args['id']
    command="sudo " + gpio + " write " + str(pin_no) + " " + value
    r, c = execute(command.replace("\n", "")) #protect command from newlines
    status, code = execute(gpio + ' readalljson');
    
def set_pin_direction(args):
    direction = args['direction']
    pin_no = args['id']
    command = "sudo " + gpio + " mode " + str(pin_no) + " " + direction
    r, c = execute(command.replace("\n", ""))
    status, code = execute(gpio + ' readalljson');

def main():
    form = cgi.FieldStorage()
    
    def op_dispatch(form):
    op = form.getfirst("op")
    args = dict((k, form[k].value) for k in form.keys() if not k=="op")
    
    op_dict = {
        "direction" : partial(get_volume, args=args),
        "value" : partial(set_volume, args=args),
    }

    op_func = op_dict.get(op, error)
    composeJS(op_func())
            

    
        
if __name__ == '__main__':
    main()
