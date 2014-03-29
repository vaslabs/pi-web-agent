import subprocess
import sys
import os

def parseStatus(status):
    if (status == "-"):
        return False
    if (status == "+"):
        return True
    return None

class Service(object):
    
    def __init__(self, line):
        parts=line.split();
        self.status=parseStatus(parts[1])
        self.name=parts[3]
        
        
    def getView(self):
        '''
        returns the html representation of a service
        '''
        row='<tr>\n<td>'
        row+=self.name
        row+='</td>'
        row+='<td>\n'
        row+='<div class="onoffswitch">\n'
        row+='<input type="checkbox" name="'+self.name+'" onclick="submit_function(this)" class="onoffswitch-checkbox" id="'
        row+=self.name + '"'
        if self.status == None:
            row+='disabled="disabled">'
        elif self.status:
            row+=' checked>'
        else:
            row+='>'
        row+='<label class="onoffswitch-label" for="'+self.name+'">\n'
        row+='<div class="onoffswitch-inner"></div>\n'
        row+='<div class="onoffswitch-switch"></div>\n'
        row+='</label>\n'
        row+='</div>\n'
        row+='</td>\n'
        row+='</tr>\n'
        return row

def serviceManagerBuilder():
    '''
    Executes chkconfig to get information for 
    all services, and builds a ServiceManager
    which contains the Services converted from each
    line of the chkconfig result
    '''
    sp=subprocess.Popen('sudo service --status-all', stdout=subprocess.PIPE, shell=True)
    output, _ = sp.communicate()
    sp.wait()
    lines=output.split('\n')
    del lines[-1]
    sm=ServiceManager(lines)
    return sm    

class ServiceManager(object):
    '''
    Holds all the information of the services. The main body
    of the app and functionality is or will be here.
    Unfinished
    '''
    def __init__(self, lines):
        self.services={}
        for line in lines:
            service=Service(line)
            self.services[service.name]=service
            
    def getView(self):
        '''
        Returns the html representation of the
        service manager. It's the main body of this
        sub-application
        '''
        div='\n<table>\n'
        div+='<tr><th>Service</th>\n'
        div+='<th>Status</th>\n'
        div+='</tr>\n'
        
        for service in self.services:
            div+=self.services[service].getView()

        div+='</table>\n'

        return div
        

    
