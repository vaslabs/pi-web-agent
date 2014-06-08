#!/usr/bin/python
from gpio_manager import *

gpio="/usr/local/bin/gpio"

leftPins = ['3V3', 'SDA', 'SCL', 'GPIO7', '0v', \
'GPIO0', 'GPIO2','GPIO3', '3v3','MOSI', \
'MISO','SCLK','0v']

rightPins = ['5V', '5v', 'GND', 'TxD', 'RxD', \
'GPIO1', '0v','GPIO4','GPIO5', \
'0v','GPIO6','CE0','CE1']


def main():

    leftDirectionPins, rightDirectionPins = getDirections()
    leftValuesPins, rightValuesPins = getValues()
    
    gpio_left = []
    counter = 0
    
    for leftPin in leftPins:
        pin_state = {}
        pin_state["name"] = leftPin
        pin_state["direction"] = leftDirectionPins[counter]
        pin_state["value"] = leftValuesPins[counter]
        gpio_left.append(pin_state)
        counter += 1
    
    gpio_right = []
    counter = 0
    
    for rightPin in rightPins:
        pin_state = {}
        pin_state["name"] = rightPin
        pin_state["direction"] = rightDirectionPins[counter]
        pin_state["value"] = rightValuesPins[counter]
        gpio_right.append(pin_state)
        counter += 1
        
    gpio = [gpio_left, gpio_right]
        
    composeJS(gpio)
        
if __name__ == '__main__':
    main()
