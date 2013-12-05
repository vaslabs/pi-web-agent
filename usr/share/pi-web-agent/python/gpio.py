#!/usr/bin/python
from RPi import GPIO 
import sys
def setup():
    GPIO.setmode(GPIO.BOARD)
    return True
    
def pin2Output(pin):
    GPIO.setup(pin, GPIO.OUT)
    return True
def pin2Input(pin):
    GPIO.setup(pin, GPIO.IN)
    return True
def activate(pin):
    GPIO.output(pin, GPIO.HIGH)
    return True
    
def deactivate(pin):
    GPIO.output(pin, GPIO.LOW)
    return True
    
def direction(pin):
    return GPIO.gpio_function(pin)
        
def isActive(pin):
    return GPIO.input(pin)    

leftPins = ['3V3', 'GPIO0', 'GPIO1', 'GPIO4', 'Reserved', \
'GPIO17', 'GPIO21','GPIO22', 'Reserved','GPIO10', \
'GPIO9','GPIO11','Reserved']

rightPins = ['5V', 'Reserved', 'GND', 'GPIO14', 'GPIO15', \
'GPIO18', 'Reserved','GPIO23','GPIO24', \
'Reserved','GPIO25','GPIO8','GPIO7']
function_map={'setup':setup, 'clean':clear}

function_map_arg = {'out':pin2Output,\
        'activate':activate, 'deactivate':deactivate,\
        'state':isActive, 'direction':direction,\
        'in':pin2Input, 'on':activate, 'off':deactivate} 
            
def clear():
    GPIO.cleanup()
    
if __name__ == '__main__':
    main(sys.argv[1:])
        
