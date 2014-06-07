#!/usr/bin/python
from pi_iptables import *

class UpdateManagerAPI(IPTablesManager):
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
    
    f = open(os.environ['MY_HOME'] + '/html/iptables_overlay_html', 'r')
    html_tables= f.read()
    f.close()

    chain_els=[[]]
    iptables=IPTablesManager()
    header_list=['protocol', 'target', 'otherinfo','destination', 'source', 'option']
    for chain in iptables.chains:
        html_tables+='<h4><a href="javascript:open_iptables_panel(\'' + chain + '\')">' + chain + '</a>'+' (Default Protocol: ' \
                        + iptables.chains[chain].policy + ')</h4>'
        if iptables.chains[chain]._isRulesEmpty():
            chain_els.append(['--','--','--','--','--','--'])
        else:
            for rule in iptables.chains[chain].rules:
                chain_els.append(list(rule.values()))
        html_tables+=HTML.table(chain_els, header_row=header_list)
        chain_els=[[]]
        html_tables+='</br>'
    
    js_status = {"IPTables":html_tables}
    composeJS(updMgr.getJS)

if __name__ == '__main__':
    main()
