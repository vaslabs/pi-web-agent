#!/usr/bin/python
import cgi
import os, sys
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME'] + '/etc/config')
from framework import view, output, get_template

def main():
    tFile = open(get_template('file_manager_controller'))
    content = tFile.read()
    tFile.close()
    view.setContent('File manager', content)
    output(view, cgi.FieldStorage())
if __name__ == "__main__":
    main()
