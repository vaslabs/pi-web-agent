#!/usr/bin/python
from pi_iptables import *
sys.path.append(os.environ['MY_HOME']+'/cgi-bin')
from HTMLPageGenerator import composeJS
import json

class IPTablesManagerAPI(IPTablesManager):
    def getJS(self):
        iptables_json={}
        self.chains={}
        list_chains, exit_code = execute("sudo iptables -n -L | grep 'Chain' | cut -d ' ' -f 2")
        lines = list_chains.split('\n')
        for line in lines[0:len(lines)-1]:
            chain_body, exit_code = execute("sudo iptables -S " + line)
            self.chains[line]=Chain(chain_body)
            iptables_json[line]={'rules': self.chains[line].rules, 'default': self.chains[line].policy}
        return iptables_json

def main():

    form = cgi.FieldStorage()
    
    iptables=IPTablesManagerAPI()
   
    composeJS(json.dumps(iptables.getJS()))

if __name__ == '__main__':
    main()
