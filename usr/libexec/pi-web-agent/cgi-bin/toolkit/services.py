import subprocess
import sys
import os
import re
def serviceBuilder(line):
    '''
    gets a line of a description of
    a service and converts it to a
    Service object
    '''
    parts=line.split();
    name=parts[0]
    levels=[]
    for i in range(1, len(parts)):
        pp=parts[i].split(':')
        if pp[1]=="on":
            levels.append(True)
        else:
            levels.append(False)
    ss=Service(name, levels)
    return ss

class Service(object):
    
    '''
    Service manages a service. Each service has
    a name and a status for each level.
    '''
    def __init__(self, name, statuses):

        self.name=name.rstrip(' ')
        self.statuses=statuses  
        self.enabled=False
        self.view=self.getView()
        
    def getView(self):
        '''
        returns the html representation of a service
        '''
        row='<tr>\n<td>'
        row+=self.name
        row+='</td>'
        counter=0
        row+='<td>\n'
        first=0
        for status in self.statuses:
            my_id=self.name+str(counter)
            if status:
                
                if not first == 0:
                    row+=', '    
                row+=str(counter)
                first+=1    
                if counter == 3:
                    self.enabled = True
            counter+=1
        row+='\n</td>\n'
        row+='\n<td>\n'
        row+='<div class="onoffswitch">\n'
        row+='<input type="checkbox" name="'+self.name+'" onclick="submit_function(this)" class="onoffswitch-checkbox" id="'
        row+=self.name + '"'
        if self.enabled:
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
    sp=subprocess.Popen('chkconfig -l', stdout=subprocess.PIPE, shell=True)
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
            service=serviceBuilder(line)
            self.services[service.name]=service
            
    def getView(self):
        '''
        Returns the html representation of the
        service manager. It's the main body of this
        sub-application
        '''
        div='\n<table>\n'
        div+='<tr><th>Service</th>\n'
        div+='<th>Levels</th>\n'
        div+='<th>Enabled</th>\n'
        div+='</tr>\n'
        
        for service in self.services:
            div+=self.services[service].view

        div+='</table>\n'

        return div
        

    
