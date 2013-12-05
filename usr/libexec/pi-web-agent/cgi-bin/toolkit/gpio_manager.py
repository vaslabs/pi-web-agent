#!/usr/bin/python
import cgi
import cgitb
import os
cgitb.enable()
import sys
from RPi import GPIO
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME']+'/scripts')
sys.path.append(os.environ['MY_HOME']+'/etc/config')
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/chrome')
sys.path.append(os.environ['MY_HOME']+'/cgi-bin')
from framework import view, config
from HTMLPageGenerator import *
from BlueprintDesigner import *
from live_info import execute
import HTML


leftPins = ['3V3', 'GPIO0', 'GPIO1', 'GPIO4', 'Reserved', \
'GPIO17', 'GPIO21','GPIO22', 'Reserved','GPIO10', \
'GPIO9','GPIO11','Reserved']

rightPins = ['5V', 'Reserved', 'GND', 'GPIO14', 'GPIO15', \
'GPIO18', 'Reserved','GPIO23','GPIO24', \
'Reserved','GPIO25','GPIO8','GPIO7']

def export_all_pins():
    for pin in leftPins:
        pinNo = name2PinNo(pin)
        if pinNo >= 0 :
            msgInitialize, errorcode=execute("sudo gpio.py in " + str(pinNo))

    for pin in rightPins:
        pinNo = name2PinNo(pin)
        if pinNo >= 0 :
            msgInitialize, errorcode=execute("sudo gpio.py in " + str(pinNo))

def name2PinNo(pin_name):
    gpio_index = pin_name.split('GPIO')
    if (len(gpio_index) <= 1):
        return -1
    isLeft = pin_name in leftPins
    if isLeft:
        leftIndex = leftPins.index(pin_name)
        return (leftIndex*2)+1
    isRight = pin_name in rightPins
    if isRight:
        rightIndex = rightPins.index(pin_name)
        return (rightIndex+1)*2
    return -1
    
def getDirections():
    leftDirections = []
    for pin in leftPins:
        pinNo = name2PinNo(pin)
        if pinNo >= 0:
            msgInitialize, errorcode=execute("sudo gpio direction " + str(pinNo))
            leftDirections.append(msgInitialize)
        else:
            leftDirections.append(pin)
            
    rightDirections = []
    for pin in rightPins:
        pinNo = name2PinNo(pin)
        if pinNo >= 0 :
            msgInitialize, errorcode=execute("sudo gpio direction " + str(pinNo))
            rightDirections.append(msgInitialize)
        else :
            rightDirections.append(pin)
                            
    return leftDirections, rightDirections  
    
def getValues(leftDirections, rightDirections):

    leftValues = []
    for pin in leftPins:
        pinNo = name2PinNo(pin)
        if pinNo >= 0 :
            msgInitialize, errorcode=execute("sudo gpio.py state " + str(pinNo))
            leftValues.append(msgInitialize)
        else :
            leftValues.append(pin)
            
    rightValues = []
    for pin in rightPins:
        pinNo = name2PinNo(pin)
        if pinNo >= 0:
            msgInitialize, errorcode=execute("sudo gpio.py state " + str(pinNo))
            rightValues.append(msgInitialize)
        else :
            rightValues.append(pin)                
    return leftValues, rightValues


def getFieldTexts(index, left_Pins, left_Direction_Pins, left_Values_Pins):
    if len(left_Pins[index].split('GPIO')) > 1 :
        direction = left_Direction_Pins[index]
        value = left_Values_Pins[index]
        generalText = '<div class="onoffswitch">\n'
        directionText ='<input type="checkbox" id="D'+left_Pins[index]
        valueText = '<input type="checkbox" id="V'+left_Pins[index]
            
        directionAttributeText = '" onclick="submit_gpio_direction(this)" class="onoffswitch-checkbox" name="'+left_Pins[index]+'" direction="' + direction + '" value="' + value + '"'
        valueAttributeText = '" onclick="submit_gpio_value(this)" class="onoffswitch-checkbox" name="'+left_Pins[index]+'" direction="' + direction + '" value="' + value + '"'


        directionText = generalText + directionText + directionAttributeText
        
        if direction == GPIO.IN :
            directionText += ' >'
        else:
            directionText += ' checked>'
        
        
        valueText = generalText + valueText + valueAttributeText
        if value == GPIO.HIGH :
            valueText += ' checked>'
        else :
            valueText += ' >'

        directionLabelText = '<label class="onoffswitch-label" for="D'+left_Pins[index]+'">\n'
        valueLabelText = '<label class="onoffswitch-label" for="V'+left_Pins[index]+'">\n'
        labelText = '<div class="onoffswitch-inner"></div>\n'
        labelText += '<div class="onoffswitch-switch"></div>\n'
        labelText += '</label>\n'
        labelText += '</div>\n'
        directionSummary = directionText + directionLabelText + labelText
        valueSummary = valueText + valueLabelText + labelText
        return directionSummary, valueSummary
    else :
        directionText="<span class=\"label label-warning\">" +left_Pins[index]+"</span>"
        directionSummary = directionText
        valueSummary = 'N/A'
        return directionSummary, valueSummary

def main():

    export_all_pins()
    form = cgi.FieldStorage()

    
    leftValuesPins, rightValuesPins = getValues()
    
    leftDirectionPins, rightDirectionPins = getDirections()
    
    pins = [[]]
    text = ''
    
    for index in range(len(leftPins)):
        leftDirectionText, leftValuesText = getFieldTexts(index, leftPins, leftDirectionPins, leftValuesPins)
        pins.append( [ leftDirectionText, leftValuesText, leftPins[index] ] )

    
    for index in range(len(rightPins)):
        rightDirectionText, rightValuesText = getFieldTexts(index, rightPins, rightDirectionPins, rightValuesPins)
        pins[index+1]+=[rightPins[index], rightValuesText, rightDirectionText ]

    html_code='<div style="clear: both">'+\
    '<h4 style="float: left">RPi.GPIO version: ' + str(GPIO.VERSION) + '</h4>'+\
    '<h4 style="float: right">RPi Board Revision: ' + str(GPIO.RPI_REVISION) + '</h4>' +\
    '</div>' +\
    '<hr />'
    html_code += '<div id="gpio_table">\n'
    html_code += HTML.table( pins, header_row=[ 'DIRECTION', 'VALUE', 'LEFT', 'RIGHT', 'VALUE', 'DIRECTION' ] )
    html_code += '</div>\n'
    html_code += '<center><div id="user_space"></div><button class="btn btn-primary" onclick="gpio_clear()">Cleanup GPIO</button></center>' 
    view.setContent('GPIO Manager', html_code)
    view.output()
    
if __name__ == '__main__':
    main()
