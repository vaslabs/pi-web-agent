#!/usr/bin/python
import os, sys, re

if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/toolkit')
sys.path.append(os.environ['MY_HOME'] + '/cgi-bin/chrome')
from live_info import execute
from services import *
from view import *
from cern_vm import Configuration
import cgi
import cgitb
from subprocess import Popen, PIPE
import HTML
cgitb.enable()

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
            #print "WHAAAT: ", line
            chain_body, exit_code = execute("sudo iptables -n -L " + line)
            #print chain_body
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
        #print "BODY: ", self.body
        body_lines = self.body.split("\n")
        for line in body_lines[0:len(body_lines)-1]:
            if line_no==0:
                #print "LINE: ", line
                find_policy = re.split(" \(|\)\n| ", line)
                #print "CHAIREPOLICY: ", find_policy
                self.type=find_policy[1]
                self.policy=find_policy[3]
                line_no+=1
            elif line_no==1:
                line_no+=1
            else:
                line_no+=1
                split_rule=line.split()
                #print "Print rules: ", split_rule
                target=split_rule[0]
                prot=split_rule[1]
                opt=split_rule[2]
                source=normalise_ipsource(split_rule[3])
                dest=split_rule[4]
                #print "No of rules: ", len(split_rule)
                if len(split_rule)>5:
                    otherinfo=split_rule[5:]
                else:
                    otherinfo="--"
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
    Application to dipplay the iptables of raspberry to the user
    '''

    form = cgi.FieldStorage()
    
    sm=serviceManagerBuilder()
    config=Configuration()
    view = View(config.system.actions)

    #this is only for modifying iptables
    html_add_rule='<p></br>Choose action</br></p>'\
                    +'<form name="inputRule">'\
                    +'<select id="selectAction" class="form-control">'\
                        +'<option>Accept</option>'\
                        +'<option>Drop</option>'\
                        +'<option>Flush</option>'\
                    +'</select>'\
                    +'<select id="selectProtocol" class="form-control">'\
                        +'<option>ALL</option>'\
                        +'<option>TCP</option>'\
                        +'<option>UDPLITE</option>'\
                        +'<option>ICMP</option>'\
                        +'<option>ESP</option>'\
                        +'<option>AH</option>'\
                        +'<option>SCTP</option>'\
                    +'</select>'\
                    +'<input type="submit" value="Submit">'\
                    +'</form>' 
            
    
    html_tables='<div id="ip_overlay" style="display: none;">' +\
                '<div><h2>Add Rules</h2>'\
                + html_add_rule +'</div></div>'

    chain_els=[[]]
    iptables=IPTablesManager()
    header_list=['protocol', 'target', 'otherinfo','destination', 'source', 'option']       
    for chain in iptables.chains:
        html_tables+='<h4>' + chain +\
         ' (Default Protocol: ' \
                      + iptables.chains[chain].policy + '</h4>'
        if iptables.chains[chain]._isRulesEmpty():
            chain_els.append(['--','--','--','--','--','--'])
        else:
            for rule in iptables.chains[chain].rules:
                chain_els.append(list(rule.values()))  
        html_tables+=HTML.table(chain_els, header_row=header_list)
        chain_els=[[]]
        html_tables+='</br>'
    
    view.setContent('IPTables', html_tables)
    view.output()

if __name__ == '__main__':
    main()
