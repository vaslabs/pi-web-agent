#!/usr/bin/python
import sys
import os
import json
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME'] + '/cgi-bin')
sys.path.append(os.environ['MY_HOME'] + '/cgi-bin/toolkit')
sys.path.append(os.environ['MY_HOME'] + '/cgi-bin/chrome')
sys.path.append(os.environ['MY_HOME'] + '/etc/config')
sys.path.append(os.environ['MY_HOME']+'/objects')
import cgi
import cgitb
from subprocess import Popen, PIPE
cgitb.enable()
from live_info import execute, getAptBusy
from framework import output, view, getDependencies
from HTMLPageGenerator import composeJS
import json
from pm_api import check_installed

PACKAGES_LIST_PATH=\
"/usr/libexec/pi-web-agent/etc/config/pm/recommendationsList.txt"
STOP = {'STOP': 'There are no more packages to load'}
    
class PackageManager(object):


    def getDpkgInfo(self, pName, fieldName) :
        bashCommand = "apt-query " + pName + " " + fieldName
        output, errorcode = execute( bashCommand )
        if output == "" :
          return fieldName + " not available"
        return output
    
    def getPkgData(self, pName):
        installed = check_installed({'key':pName})
        
        descriptionText = self.getDpkgInfo( pName, "Description" )
        versionText = self.getDpkgInfo( pName, "Version" )
        package = {'Package Name':pName, 'Description':descriptionText, 'Version':versionText, 'installed':installed['installed']}    
        return package
    
    def loadPackages(self, packages):
        self.packages = {}
        for package in packages:
            self.packages[package] = self.getPkgData(package)
        

def main():
    form = cgi.FieldStorage()
    if not 'p' in form:
        view.setContent('Dependency Manager', 'This is the dependency manager for pi-web-agent extensions')     
        output(view, form)
    else:
        pm = PackageManager()
        dependencies = getDependencies(form['p'].value)
        pm.loadPackages(dependencies)
        composeJS(json.dumps(pm.packages))
               
if __name__ == '__main__':
    main()

