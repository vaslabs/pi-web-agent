#!/usr/bin/python
import pygame
from pygame import Surface
import cgi, cgitb
cgitb.enable()

def compose_image_document(image):
    PATH="/usr/share/pi-web-agent/camera-media/"
    img=open(PATH+image)
    print "Content-type: image/png"
    print
    print img.read()
    
def main():
    form = cgi.FieldStorage()
    return compose_image_document(form['image'].value)
    
if __name__ == "__main__":
    main()
    
