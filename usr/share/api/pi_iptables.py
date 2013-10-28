#!/usr/bin/python
import os, sys, re

if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/toolkit')
from live_info import execute

class IPTablesManager(object):

    def __init__(self):
        self.chains={}
        list_chains, exit_code = execute("sudo iptables -L | grep 'Chain' | cut -d ' ' -f 2")
        lines = list_chains.split('\n')
        for line in lines[0:len(lines)-1]:
            #print "WHAAAT: ", line
            chain_body, exit_code = execute("sudo iptables -L " + line)
            #print chain_body
            self.chains[line]=Chain(chain_body)
        
    def __str__(self):
        message=""
        for chain in self.chains:
            message+=chain + "\n"
            message+=str(self.chains[chain]) +"\n"
        return message

class Chain(object):
    def __init__(self, body):
        self.body = body
        self.policy=''
        self.type=''
        self.rules=[]
        self._parseChain()

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
                source=split_rule[3]
                dest=split_rule[4]
                #print "No of rules: ", len(split_rule)
                if len(split_rule)>5:
                    otherinfo=split_rule[5:]
                else:
                    otherinfo=""
                rule={'target':target, 'protocol':prot, 'option':opt, 'source':source, 'destination':dest, 'otherinfo':otherinfo}
                self.rules.append(rule)

    def __str__(self):
        return "Policy: " + self.policy + "\n" +\
               "Type: " + self.type + "\n" +\
               str(self.rules)
