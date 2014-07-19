#!/usr/bin/python
CONFIG_FILE='/usr/share/pi-web-agent/startup/startup.cfg'

import os
import sys
import subprocess
import json

def execute_next(command):
    os.spawnl(os.P_NOWAIT, command)
    
def load_and_fire_startup_apps():
    jFile = open(CONFIG_FILE)
    data = json.load(jFile)
    for script_def in data:
        command = script_def['script'] + ' ' + script_def['args']
        execute_next(command)
    
def main():
    load_and_fire_startup_apps()
    
if __name__ == "__main__":
    main()
