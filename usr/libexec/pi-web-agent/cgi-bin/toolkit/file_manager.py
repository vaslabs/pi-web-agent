#!/usr/bin/python
import json
from live_info import execute
import cgi, cgitb
cgitb.enable()
from HTMLPageGenerator import composeJS
def parseFile(entry):
    #-rw-r--r-- 1 pi pi   129 Mar 23 22:56 AUTHORS
    if (len(entry) == 0):
        return None
    parts = entry.split()
    permissions = parts[0][1:]
    type_of_entry = parts[0][0]
    user=parts[2]
    group=parts[3]
    size_in_bytes = parts[4]
    date = {'month':parts[5], 'day':parts[6]}
    if ':' in parts[7]:
        date['time'] = parts[7]
    else:
        date['year'] = parts[7]
    file_name = parts[8]
    
    for parts_left in parts[9:]:
        file_name += " " + parts_left
        
    return {'type':type_of_entry, 'permissions':permissions,\
     'owner':user, 'group':group, 'size':size_in_bytes, 'date':date,\
      'name':file_name}
            

def getContents(path):
    contents, _ = execute("sudo ls -l " + path)
    contents = contents.split("\n")[1:len(contents)]
    files = []
    for content in contents:
        entry = parseFile(content)
        if entry != None:
            files.append(entry)
    return files
    
def main():
    form = cgi.FieldStorage()
    if not 'path' in form:
        composeJS('[error]')
    path = form['path'].value
    contents = getContents(path)
    composeJS(json.dumps(contents))
    return

if __name__ == "__main__":
    main()
