#!/usr/bin/python
from camera_manager import CameraManager
import json
from framework import composeJS
import cgi

def get_images():
    cMgr = CameraManager()
    json_data = cMgr.getImages()
    return json.dumps(json_data)
    
    
def main(arg):
    switch = {'gallery': get_images}
    composeJS(switch[arg]())
    
    
if __name__ == "__main__":
    form = cgi.FieldStorage()
    
    if (len(form) < 1):
        composeJS([len(form)])
    else: 
        main(form['cmd'].value)
