#!/usr/bin/python
import os, sys, re

if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/toolkit')
sys.path.append(os.environ['MY_HOME'] + '/etc/config')

from live_info import execute
import cgi
import cgitb

cgitb.enable()
from framework import output, view, get_template

def normalise_ipsource(source):
    MAX_FIELDS=4
    postfix='...'
    ip_fields = source.split('.')
    counter = 0
    normalised_source = ""
    for field in ip_fields:
        if (counter >= 4):
            break
        if (counter > 0):
            normalised_source+='.'
        normalised_source+=field
        counter+=1
    if len(ip_fields) > counter:
        normalised_source+=postfix
    return normalised_source


def normalise_ipsource(source):
    MAX_FIELDS=4
    postfix='...'
    ip_fields = source.split('.')
    counter = 0
    normalised_source = ""
    for field in ip_fields:
        if (counter >= 4):
            break
        if (counter > 0):
            normalised_source+='.'
        normalised_source+=field
        counter+=1
    if len(ip_fields) > counter:
        normalised_source+=postfix
    return normalised_source


class IPTablesManager(object):

    def __init__(self):
        self.chains={}
        list_chains, exit_code = execute("sudo iptables -n -L | grep 'Chain' | cut -d ' ' -f 2")
        lines = list_chains.split('\n')
        for line in lines[0:len(lines)-1]:
            chain_body, exit_code = execute("sudo iptables -S " + line)
            self.chains[line]=Chain(chain_body)
        
    def __str__(self):
        message=""
        for chain in self.chains:
            message+=chain + "\n"
            message+=str(self.chains[chain]) +"\n"
        return message

    def addRule(self):
        pass
        

class Chain(object):
    def __init__(self, body):
        self.body = body
        self.policy=''
        self.type=''
        self.rules=[]
        self._parseChain()

    def _isRulesEmpty(self):
        if not self.rules:
            return 1
        else:
            return 0
    
    def _parseChain(self):
        line_no = 0
        body_lines = self.body.split("\n")
        for line in body_lines[0:len(body_lines)-1]:
            if line_no==0:
                new_action = line.split()
                self.type = new_action[1]
                try:
                    self.policy = new_action[2]
                except:
                    self.policy = "--"
                line_no+=1
            else:
                split_rule = re.split(" -", line)
                source="ALL"
                dest="ALL"
                otherinfo="--"
                opt="--"
                prot="--"
                target="--"
                for rule_params in split_rule:
                    split_parameters = rule_params.split()
                    if split_parameters[0] == 'p':
                        prot=split_parameters[1]
                    elif split_parameters[0] == 'j':
                        target=split_parameters[1]
                    elif split_parameters[0] == 's':
                        source=normalise_ipsource(split_parameters[1])
                    elif split_parameters[0] == 'd':                
                        dest=split_parameters[1]
                
                rule={'target':target, 'protocol':prot, 'option':opt,\
                      'source':source, 'destination':dest, 'otherinfo':otherinfo}
                self.rules.append(rule)

    def __str__(self):
        return "Policy: " + self.policy + "\n" +\
                "Type: " + self.type + "\n" +\
                str(self.rules)

    #executes the command to add a new protocol rule
    def addProtocolRule(self, chain, action, protocol):
        self.message=os.system('sudo iptables -A ' +\
                                chain + ' -p ' + protocol + ' ' + action)


def main():
    '''
Application to display the iptables of raspberry to the user
'''

    form = cgi.FieldStorage()
    
    f = open(get_template('firewall_controller'))
    html_tables= f.read()
    f.close()

    view.setContent('IPTables', html_tables)
    output(view, form)

if __name__ == '__main__':
    main()
