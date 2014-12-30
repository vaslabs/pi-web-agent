#!/usr/bin/python
import json
import os, sys
from live_info import execute
import cgi, cgitb
import ast
cgitb.enable()
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME'] + '/etc/config')

from HTMLPageGenerator import composeJS
from framework import view, output
from functools import partial
import re
import subprocess
from live_info import package_is_installed

def search_package(args):
    package_name = args['key']
    out, code = execute('apt-cache search --names-only ' + package_name)
    package_list = out.split('\n')
    packages={}
    if (len(package_list) > 0):
        package_list = package_list[:-1]
    else:    
        return {}
    for entry in package_list:
        name=entry.split(' ')[0]
        description=entry[len(name)+3:]
        packages[name] = description
    return packages

def check_installed(args):
    package_name = args['key']
    return {'installed':package_is_installed(package_name)}

def check_group_installed(args):
    package_group = {}
    try:
        packages = json.loads(str(args['packages']))
    except:
        try:
            packages = ast.literal_eval(str(args['packages']))
        except Exception as e:
            return {'status':'REQUEST_ERROR', 'code':-1, 'structure':str(args['packages']), 'msg':str(e), 'allargs':str(args)}
        
    for pkg in packages:
        if not pkg in package_group:
            package_group[pkg] = {}
            package_group[pkg]['installed'] = package_is_installed(pkg)
            
    return package_group

def error():
    return json.dumps("Error")


def op_dispatch(form):
    op = form.getfirst("op")
    args = dict((k, form[k].value) for k in form.keys() if not k=="op")
    
    op_dict = {
        'search': partial(search_package, args=args),
        'check_group': partial(check_group_installed, args=args)
    }

    op_func = op_dict.get(op, error)
    composeJS(json.dumps(op_func()))
    
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
