#!/usr/bin/python
import json
import os, sys
from live_info import execute
import cgi, cgitb
cgitb.enable()
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME'] + '/etc/config')

from framework import view, output, composeJS
from functools import partial
import re
import subprocess

class FileSystemObject(object):

    def __init__(self, name, parent, size, children):
        # name :: str
        # parent :: str - parent's name not ref to parent
        # size :: int
        # children :: List[FileSystemObject]
        self.name = name
        self.parent = parent
        self.size = size
        self.children = children

        
class DefaultEncoder(json.JSONEncoder):

    def default(self, o):
        return o.__dict__

def traverse_fs(root, parent="", n_levels=3):
    # root :: str
    # parent :: str
    # n_level :: int
    #
    # Returns FileSystemObject - root of fs tree
    #
    # for now ignore n_levels
    from os.path import getsize
    from os.path import join
    
    names = os.listdir(root)
    dirs, files = list(), list()
    
    for f in names:
        if os.path.isfile(join(root, f)):
            files.append(f)
        else:
            dirs.append(f)

    children = list(FileSystemObject(f, root, getsize(join(root, f)), list()) for f in files)

    for name in dirs:
        n_root = join(root, name)
        children.append(traverse_fs(root=n_root, parent=root))
    
    dir_size = sum(f.size for f in children)

    return FileSystemObject(root, parent, dir_size, children)

    
def get_chart_format(root_dir):
    # root_dir :: FileSystemObject
    #
    # Returns: entry_list :: List[List[str]]
    from collections import deque
    
    to_process = deque()
    entry_list = list()
    
    to_process.append(root_dir)
    while to_process:
        f = to_process.popleft()
        entry_list.append([f.name, f.parent, f.size])

        for child in f.children:
            to_process.append(child)

    return entry_list


def get_usage(top):
    # top :: str
    # Returns fs_items:: List[(str, str, int)]
    #
    import os
    from os.path import join, getsize
    
    dir_size = 0
    fs_items = list()
    fs_items.append([top, None, 0])
              
    for root, dirs, files in os.walk(top):
        for file in files:
            fname = join(root, file)
            try:
                size = getsize(fname)
                fs_items.append([fname, root, size])
            except OSError:
                pass

        for dir in dirs:
            dname = join(root, dir)
            fs_items.append([dname, root, dir_size])

    return json.dumps(fs_items)


def error():
    return json.dumps("Error")


def op_dispatch(form):
    # Do a dispatch on the operation, only one so far though so...!
    op = form.getfirst("op")
    args = dict((k, form[k].value) for k in form.keys() if not k=="op")

    op_dict = {
        "get_usage" : partial(get_usage, args['top'])
    }

    op_func = op_dict.get(op, error)
    composeJS(op_func())

    
def main():
    form = cgi.FieldStorage()
    try:
	op_dispatch(form)
    except:
    	composeJS(error())
if __name__ == "__main__":
    main()



### test stuff, they should probably go in the /tests dir
### or become unit tests whatever
def main_test():
    root_dir = traverse_fs("/Users/argyris/workspace/dir_test/dir1/")
    entry_list = get_chart_format(root_dir)
    entry_list_json = DefaultEncoder().encode(entry_list)
    
    return entry_list_json

def main_test_walk():
    fs_items = get_usage("/home/rpi/")
    return json.dumps(fs_items)
        
