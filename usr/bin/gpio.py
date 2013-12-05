#!/usr/bin/python
from RPi import GPIO 

def setup():
    GPIO.setmode(GPIO.BCM)
    
def pin2Output(pin):
    GPIO.setup(pin, GPIO.OUT)

def pin2Input(pin):
    GPIO.setup(pin, GPIO.IN)

def activate(pin):
    GPIO.output(pin, GPIO.HIGH)

def deactivate(pin):
    GPIO.output(pin, GPIO.LOW)

def direction(pin):
    print GPIO.gpio_function(pin)
        
def isActive(pin):
    if GPIO.input(pin) == GPIO.HIGH:
        print 1
    print 0    
    
def clear():
    GPIO.cleanup()
    
def main(args):
    function_map={'setup':setup(), 'out':pin2Output(args[1]),\
        'activate':activate(args[1]), 'deactivate':deactivate(args[1]),\
        'state':isActive(args[1]), 'clean':clear, 'direction':direction(args[1]),
        'in':pin2Input(args[1]), 'on':activate(args[1]), 'off':deactivate(args[1])} 
    try:
        function_map[args[0]]
    except:
        sys.exit(2)        
    
if __name__ == '__main__':
    main(sys.argv[1:])
        
