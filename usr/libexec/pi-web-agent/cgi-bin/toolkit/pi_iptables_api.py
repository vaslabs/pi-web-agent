#!/usr/bin/python
from pi_iptables import *
sys.path.append(os.environ['MY_HOME']+'/cgi-bin')
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/chrome')
from view import composeJS
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

    def flushRules(self, chain):
        if chain=="all":
            chain = ""
            
        command = "sudo iptables -F {chain_name}"
        out, exit_code = execute(command.format(chain_name = chain))

        return {"code":0}

def main():
    form = cgi.FieldStorage()
    iptables=IPTablesManagerAPI()
    
    if "flush" in form:
        chain = form.getfirst("flush")
        composeJS(json.dumps(iptables.flushRules(chain)))
    else:
        composeJS(json.dumps(iptables.getJS()))

if __name__ == '__main__':
    main()
