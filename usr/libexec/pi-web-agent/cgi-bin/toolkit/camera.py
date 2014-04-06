#!/usr/bin/python
import sys
import os
import cgi
import cgitb

cgitb.enable()
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME']+'/cgi-bin')
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/chrome')
sys.path.append(os.environ['MY_HOME']+'/etc/config')

from framework import output, view
from live_info import hostname, execute, response

def getView():
    hostip=hostname()
    hostip=hostip[0:len(hostip) - 1]
    return '''
<div align="center">
    <object type="application/vlc" data="rtsp://''' + hostip + ''':8554/" width="400" height="300" id="video1">
         <param name="movie" value="rtsp://''' + hostip + ''':8554/"/>
         <embed type="video/ogg" name="video1"
         autoplay="yes" loop="no" width="640" height="480"
         target="rtsp://''' + hostip + ''':8554/" />
    </object>
    <table>
        <tbody>
            <tr>
              <td style="text-align: center; align: center"><button type="button" class="btn btn-primary" onclick="navigate('/cgi-bin/toolkit/camera.py?type=js')">Refresh</button></td>
              <td style="text-align: center; align: center"><button type="button" class="btn btn-warning" onclick="start_live_streaming()">Start camera</button></td>
              <td style="text-align: center; align: center"><button type="button" class="btn btn-danger" onclick="stop_live_streaming()">Stop camera</button></td>
            </tr>
        </tbody>
    </table>
</div>
'''


def main():    
    
    form = cgi.FieldStorage()
    if 'cmd' in form:
        command = form['cmd'].value
        if command == 'start':
            response("0")
            execute('start-stream-cam.sh &')
            sys.exit(0)
        elif command == 'stop':
            try:
                execute('sudo kill $(pidof raspivid)')
            except:
                pass
        response("0")
        return
    
    content=getView()
    view.setContent('Live camera', content)
    
    output(view, form)
    
if __name__ == "__main__":
    main()
