#!/usr/bin/python
import pygame
from pygame import Surface

def compose_image_document(image):
    
    img=open(image)
    print "Content-type: image/png"
    print
    print img.read()
    
def main():
    return compose_image_document('/home/pi/quokka.png')
    
if __name__ == "__main__":
    main()
    
