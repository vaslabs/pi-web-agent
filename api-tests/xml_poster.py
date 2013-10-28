#!/usr/bin/python
import xml.etree.ElementTree as ET
import os
import urllib
import urllib2
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/cernvm-appliance-agent'

def prepare():
    transaction=ET.Element('cernvm-api', {'version':'1.0'})

    username=ET.Element('username')
    username.text='admin'
    apikey=ET.Element('apikey')
    apikey.text='42a7gXpcAVWfE'
    transaction.append(username)
    transaction.append(apikey)
    return transaction
    

def test_table(transaction):
    addrequest=ET.Element('add')
    title=ET.Element('title')
    title.text='Hello Family'

    cg=ET.Element('command-group')
    command=ET.Element('command', {'title':'Hello Family', 'format':'table'})
    command.text='echo "Message Name"; echo "Hello Gabriel"; '+\
    'echo "Hello Styliani"; echo "Hello Vasiliki"; echo "Hello George"'

    addrequest.append(title)
    cg.append(command)
    addrequest.append(cg)
    transaction.append(addrequest)
    return transaction
    

def test_basic(transaction):
    addrequest=ET.Element('add')
    title=ET.Element('title')
    title.text='Hello World'

    cg=ET.Element('command-group')
    command=ET.Element('command', {'title':'Hello'})
    command.text='echo "Hello World"'

    addrequest.append(title)
    cg.append(command)
    addrequest.append(cg)
    transaction.append(addrequest)
    return transaction

    
def post(transaction):
    xml_string = ET.tostring(transaction, encoding='UTF-8')
    data = urllib.urlencode({'xml': xml_string})
    url='https://127.0.0.1:8003/cgi-bin/api/cernvm.py'
    response = urllib2.urlopen(url, data)
    for line in response.readlines():
        print line
    

def test_remove_basic(transaction):
    removerequest = ET.Element('remove')
    reqID = ET.Element('id')
    reqID.text = 'Hello World'
    removerequest.append(reqID)
    transaction.append(removerequest)
    return transaction

def test_list(transaction):
    el_list = ET.Element('list')
    transaction.append(el_list)
    return transaction

transaction=prepare()
        
'''    
ftr=test_basic(transaction)
ftr=test_remove_basic(transaction)
'''
ftr = test_list(transaction)
post(ftr)

