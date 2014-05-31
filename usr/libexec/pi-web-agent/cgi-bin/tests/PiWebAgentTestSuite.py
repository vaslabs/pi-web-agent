import os, sys
if not 'MY_HOME' in os.environ:
    os.environ['MY_HOME'] = os.environ['HOME'] + '/pi-web-agent/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME'] + '/etc/config')
sys.path.append(os.environ['MY_HOME'] + '/cgi-bin')
