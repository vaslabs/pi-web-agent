#!/usr/bin/python
from gpio_manager import *
import json

def main():
    gpio_data, code = execute(gpio + ' readalljson')
    if (code != 0):
        result={'error':code}
    else:
        result=json.loads(gpio_data)
    composeJS(json.dumps(result))
        
if __name__ == '__main__':
    main()
