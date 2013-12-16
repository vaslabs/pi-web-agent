#!/bin/usr/python
import sys
sys.path.append('/usr/share/pi-web-agent/python/')
from gpio import *
from daemon3x import Daemon
QUEUE="/usr/share/pi-web-agent/gpio.queue"
SERVED="/usr/share/pi-web-agent/gpio.stats"

class GPIODaemon(Daemon):

    def start(self):
        open(QUEUE, 'w').close()        
        Daemon.start(self)
        
    def stop(self):
        open(SERVED, 'w').close()    
        Daemon.stop(self)
            
    def run(self):
        while True:
            self.doWork()
            time.sleep(1)

    def doWork(self):
        try:
            queue=open(QUEUE, 'r')
            work=[]
            for line in queue:
                work.append(line)
            queue.close()
            if (len(work) == 0):
                open(SERVED, 'w').close()
            served=open(SERVED, 'a')
            for workpiece in work:
                self.serve(workpiece.split(), served)
            served.close()
        except:
            pass
            
    def serve(self, args, sFile):
        try:
            if args[0] in function_map:
                result=str(function_map[args[0]]())
            elif args[0] in function_map_arg:
                result=str(function_map_arg[args[0]](int(args[1])))
            else:
                result=str(False)
            sFile.write(result + '\n')
        except Exception as e:
            pass
def main(argv):
    daemon = MyDaemon('/tmp/daemon-example.pid')
    if len(argv) == 2:
        if 'start' == argv[1]:
                daemon.start()
        elif 'stop' == argv[1]:
                daemon.stop()
        elif 'restart' == argv[1]:
                daemon.restart()
        else:
                print "Unknown command"
                sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
            
if __name__ == "__main__":
    main(sys.argv)
