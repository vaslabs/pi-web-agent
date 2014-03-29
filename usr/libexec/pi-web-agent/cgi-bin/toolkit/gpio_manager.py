#!/usr/bin/python
import cgi, cgitb
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
from framework import view, config, output
from HTMLPageGenerator import *
from BlueprintDesigner import *
from live_info import execute
import HTML

gpio="/usr/local/bin/gpio"

leftPins = ['3V3', 'SDA', 'SCL', 'GPIO7', '0v', \
'GPIO0', 'GPIO2','GPIO3', '3v3','MOSI', \
'MISO','SCLK','0v']

rightPins = ['5V', '5v', 'GND', 'TxD', 'RxD', \
'GPIO1', '0v','GPIO4','GPIO5', \
'0v','GPIO6','CE0','CE1']

def name2PinNo(pin_name):
    gpio_index = pin_name.split('GPIO')
    if (len(gpio_index) <= 1):
        return -1
    return gpio_index[1]
    
def getDirections():
    leftDirections = []
    for pin in leftPins:
        pinNo = name2PinNo(pin)
        if pinNo >= 0:
            msgInitialize, errorcode=execute("sudo gpio-query direction \"GPIO " + str(pinNo) + "\"")
            leftDirections.append(msgInitialize.strip())
        else:
            leftDirections.append(pin)
            
    rightDirections = []
    for pin in rightPins:
        pinNo = name2PinNo(pin)
        if pinNo >= 0 :
            msgInitialize, errorcode=execute("sudo gpio-query direction \"GPIO " + str(pinNo) + "\"")
            rightDirections.append(msgInitialize.strip())
        else:
            rightDirections.append(pin)
                            
    return leftDirections, rightDirections  
    
def getValues():

    leftValues = []
    for pin in leftPins:
        pinNo = name2PinNo(pin)
        if pinNo >= 0 :
            msgInitialize, errorcode=execute("sudo gpio-query value \"GPIO " + str(pinNo) + "\"")
            if msgInitialize[0] == "H":
                value=GPIO.HIGH
            else:
                value=GPIO.LOW
            leftValues.append(value)
        else:
            leftValues.append(pin)
            
    rightValues = []
    for pin in rightPins:
        pinNo = name2PinNo(pin)
        if pinNo >= 0:
            msgInitialize, errorcode=execute("sudo gpio-query value \"GPIO " + str(pinNo) + "\"" )
            if msgInitialize[0] == "H":
                value=GPIO.HIGH
            else:
                value=GPIO.LOW
            rightValues.append(value)
        else:
            rightValues.append(pin)                
    return leftValues, rightValues


def getFieldTexts(index, left_Pins, left_Direction_Pins, left_Values_Pins):
    if len(left_Pins[index].split('GPIO')) > 1 :
        direction = left_Direction_Pins[index]
        value = left_Values_Pins[index]
        generalText = '<div class="onoffswitch">\n'
        directionText ='<input type="checkbox" id="D'+left_Pins[index]
        valueText = '<input type="checkbox" id="V'+left_Pins[index]
            
        directionAttributeText = '" onclick="submit_gpio_direction(this)" class="onoffswitch-checkbox" name="'+left_Pins[index]+'" direction="' + direction + '" value="' + str(value) + '"'
        valueAttributeText = '" onclick="submit_gpio_value(this)" class="onoffswitch-checkbox" name="'+left_Pins[index]+'" direction="' + direction + '" value="' + str(value) + '"'


        directionText = generalText + directionText + directionAttributeText
        
        if direction == "IN":   
            directionText += '>'
            #valueAttributeText += ' disabled="disabled"' this should be done with javascript support (on direction click, enable this checkbox)
        else:
            directionText += ' checked>'
        
        
        valueText = generalText + str(valueText) + valueAttributeText
        if int(value) == GPIO.HIGH:
            valueText += ' checked>'
        else:
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
    else:
        directionText="<span class=\"label label-warning\">" +left_Pins[index]+"</span>"
        directionSummary = directionText
        valueSummary = 'N/A'
        return directionSummary, valueSummary

def main():

    leftDirectionPins, rightDirectionPins = getDirections()
    leftValuesPins, rightValuesPins = getValues()
        
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
    output(view, cgi.FieldStorage())
    
if __name__ == '__main__':
    main()
