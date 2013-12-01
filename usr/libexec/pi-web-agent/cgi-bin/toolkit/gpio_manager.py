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

def name2PinNo(pin_name):
    gpio_index = pin_name.split('GPIO')
    if (len(gpio_index) <= 1):
        return -1
    isLeft = pin_name in leftPins
    if isLeft:
        leftIndex = leftPins.index(pin_name)
        return leftIndex
    isRight = pin_name in rightPins
    if isRight:
        rightIndex = rightPins.index(pin_name)
        return rightIndex
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
    
def getValues():
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
        if pinNo >= 0 :
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


    html_code = HTML.table( pins, header_row=[ 'DIRECTION', 'VALUE', 'LEFT', 'RIGHT', 'VALUE', 'DIRECTION' ] )

    view.setContent('GPIO Manager', html_code)
    view.output()
    
if __name__ == '__main__':
    main()



#def generate_html_code(enabled_pins):
#    html_code = ''
#       with open ("/usr/libexec/pi-web-agent/html/utilities/gpio_table.html", "r") as myfile:
#        html_code=myfile.read().replace('\n', '')
#        
#    for pin in enabled_pins:    
#        pin_off_left=html_code.find(<"td class=\"gpio_off\">OFF</td><td>" + pin + "</td>")
#        pin_off_right=html_code.find("<td>" + pin + "</td><td class=\"gpio_off\">OFF</td>")
#        if pin_off_left != -1:
#            html_code.replace("td class=\"gpio_off\">OFF</td><td>" + pin + "</td>", "td class=\"gpio_on\">ON</td><td>" + pin + "</td>")    
#        elif pin_off_right != -1:
#            html_code.replace("<td>" + pin + "</td><td class=\"gpio_off\">OFF</td>", "<td>" + pin + "</td><td class=\"gpio_on\">ON</td>")
#                
#    return html_code

#def get_default_view():
#       enabled_pins=get_enabled_pins()
#       html_code=generate_html_code(enabled_pins)
#       return html_code
