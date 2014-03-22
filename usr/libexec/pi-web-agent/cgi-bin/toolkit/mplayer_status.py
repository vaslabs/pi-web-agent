#!/usr/bin/python
import cgi
import cgitb
import os
cgitb.enable()
import sys
import subprocess
import json

def execute(command):
	sp=subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
	output, err = sp.communicate()
	sp.wait()
	return sp.returncode
	
def jsonReply(stringifiedJSON):
		print "Status: 200 OK"
		print "Content-Type: application/json"
		print "Cache-Control: no-store"
		print "Length:", len(stringifiedJSON)
		print ""
		print stringifiedJSON
		
def main():
	if (os.environ['REQUEST_METHOD']=="GET"):
		if (execute('pidof mplayer')==0):
			jsonReply("{ \"status\" : \"playing\" }")
		else:
			jsonReply("{ \"redirect\" : \"mplayer.py\" }")
		
	elif (os.environ['REQUEST_METHOD']=="DELETE"):
		if (execute ('echo "quit" > /tmp/mplayer-control')==0):
			jsonReply("{ \"redirect\" : \"mplayer.py\" }")
		else:
			jsonReply("{ \"status\" : \"stop failed\" }")
	elif (os.environ['REQUEST_METHOD']=="POST"):
		data=json.loads(sys.stdin.read())
		try:
			if 'volume' in data:
				if (0<=int(data['volume'])<=100):
					execute ( 'echo "set_property volume ' + str(data['volume'])+\
																	 '" > /tmp/mplayer-control')
					streqhelper=':'.join(map(str,data['eqhelper']))
					execute("echo '"+str(data["volume"])+"\n"+streqhelper+"' > /tmp/mplayer_status")
					jsonReply("{ \"status\" : \"volume " + str(data['volume'])+\
																								"\" }")
				else:
					jsonReply("{ \"status\" : \"Oups!In valid volume range."+\
															"Don't send castom requests!\" }")
			elif 'eq' in data:
				c=0
				for n in data['eq']:
					if (-12<=n<=12):
						c+=1
				if (c==10):		
					streq=':'.join(map(str,data['eq']))
					execute ( 'echo "af_cmdline equalizer '+streq +\
																	'" > /tmp/mplayer-control')
					execute("echo '"+str(data['volumehelper'])+"\n"+streq+"' > /tmp/mplayer_status")
					jsonReply("{ \"status\" : \"eq " + streq+ "\" }")
				else:
					streq=':'.join(map(str,data['eq']))
					jsonReply("{ \"status\" : \"Invalid eq settings[-12/12]:" +\
																					 streq+ "\" }")
		except ValueError:
			jsonReply("{ \"status\" : \"Invalid Input!Don't send custom"
																				+" requests!\" }")
	else:
		jsonReply("{ \"status\" : \"unknown operation\" }")
	
if __name__ == '__main__':
    main()  	