#!/usr/bin/python
from gpio_manager import *
import json
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/chrome')
def main():
    gpio_data, code = execute(gpio + ' readalljson')
    if (code != 0):
        result={'error':code}
    else:
        result=json.loads(gpio_data)
    composeJS(json.dumps(result))
        
if __name__ == '__main__':
    main()
