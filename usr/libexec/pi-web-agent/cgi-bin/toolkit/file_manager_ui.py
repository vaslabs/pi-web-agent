#!/usr/bin/python
import cgi
import os, sys
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME'] + '/etc/config')
from framework import view, output

def main():
    content = '''
        <ul id="bpath" class='breadcrumb' style="margin-bottom: 5px;">
        </ul>
        <table id="file-manager-table" class="table table-striped table-hover ">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Type</th>
                    <th>Modified</th>
                    <th>Owner</th>
                    <th>Group</th>
                </tr>
            </thead>
        </table>
        <script src="/css/file_manager.js" type="text/javascript"></script>
        
    '''
    view.setContent('File manager', content)
    output(view, cgi.FieldStorage())
if __name__ == "__main__":
    main()
