#!/usr/bin/env python
#the purpose of this script is to traverse 
#json configuration files given a set of 
#keys as the path to follow both array
#indexes and object keys can be used

import json
import sys

data = json.load(sys.stdin)

for key in sys.argv[1:]:
    try:
        data = data[key]
    except TypeError:  # This is a list index
        data = data[int(key)]

print(data) 
