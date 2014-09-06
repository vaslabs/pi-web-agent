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
        self.services_js = {}
        for line in lines:
            service=Service(line)
            self.services[service.name]=service
            self.services_js[service.name] = service.status    

    
