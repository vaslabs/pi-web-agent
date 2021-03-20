import pyinotify
import argparse
import os.path
import shutil

class EventHandler(pyinotify.ProcessEvent):

    def __init__(self, work_dir):
        self.work_dir = work_dir
        
    def _is_source_file(self, f):
        src_ext = set(['.py', '.html', '.js', '.htm'])
        f_name, f_ext = os.path.splitext(f)
        
        return f_ext in src_ext

    def process_IN_CLOSE_WRITE(self, event):
        d, fname = os.path.split(event.pathname)
        if self._is_source_file(fname):
            dd = event.pathname.replace(self.work_dir, "")
            dest = "".join(["/", dd])
            shutil.copy(event.pathname, dest)

def handle_change_events(work_dir):
    wm = pyinotify.WatchManager()
    mask = pyinotify.IN_CLOSE_WRITE
    handler = EventHandler(work_dir)
    notifier = pyinotify.Notifier(wm, handler)
    wdd = wm.add_watch(work_dir, mask, rec=True)

    notifier.loop()
    
def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-wd", "--work-dir", required=True)

    return parser

def command_line_runner():
    parser = get_parser()
    args = parser.parse_args()
    
    # go into a loop reacting to file change events in src files in work_dir
    handle_change_events(args.work_dir)
    
if __name__ == "__main__":
    command_line_runner()

