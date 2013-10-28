import xml.etree.ElementTree as ET
#gets ip tables manager and converts it to XML
#waiting for the actual implementation of iptables manager
class FirewallAdapter(object):
	
	def __init__(self, iptablesManager):
		self.chains = iptablesManager.chains
		
	'''
    <chain>
        <type> </type>
        <policy></policy>
        <target>
        <rules>
        <rule id="">
            <target></target>
            <protocol></protocol>
            <option></option>
            <source></source>
            <destination></destination>
            <otherinfo></otherinfo>
        </rule>
        </rules>
    </chain>
	'''
	def toXML(self):
        el_firewall = ET.Element('firewall')
        for chain in self.chains:
            el_chain=ET.Element('chain')
            el_type=ET.Element('type')
            el_policy=ET.Element('policy')
            el_target=ET.Element('target')
            el_rules=ET.Element('rules')
            
            el_type.text=chain.type
            el_policy=chain.policy
            el_target=chain.target

            el_chain.append(el_policy)
            el_chain.append(el_target)
            rule_id=0            
            for rule in chain.rules:
                el_rule=ET.Element('rule', {'id':rule_id})
                el_target=ET.Element('target')
                el_protocol=ET.Element('protocol')
                el_option = ET.Element('option')
                el_source = ET.Element('source')
                el_destination = ET.Element('destination')
                el_otherinfo = ET.Element('otherinfo')
                el_rule.append(el_target)
                el_rule.append(el_protocol)
                el_rule.append(el_option)
                el_rule.append(el_souce)
                el_rules.append(el_rule)
                rule_id+=1
            el_firewall.append(el_chain)
        return el_firewall

	def toHTML(self):
		pass #stab
	
	
	
		
