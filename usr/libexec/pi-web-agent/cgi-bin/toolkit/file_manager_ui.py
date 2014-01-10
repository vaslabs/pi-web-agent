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
                    <th>Size</th>
                </tr>
            </thead>
        </table>
        <div id="openDialog" title="Open with.">
  				<p>Choose a web-agent application to open your file with</p>
  				<ul>
  				</ul>
			</div>
				<link rel="stylesheet" href="/css/jquery-ui.css">
		<script src="/css/jquery-ui.js"></script>
		 <script src="/css/appDefinitions.js" type="text/javascript"></script>
        <script src="/css/file_manager.js" type="text/javascript"></script>
        <link href="/css/openDialog.css" type="text/css" rel="stylesheet" />
    '''
    view.setContent('File manager', content)
    output(view, cgi.FieldStorage())
if __name__ == "__main__":
    main()
