var analyzerLoc = '../toolkit/disk_analyzer.py?path=';
var spath="/home";
getContents(spath);

function redir(dirPath) {
    document.location.href = analyzerLoc + dirPath;
}

function getContents(path) {
    processing();
    url = '/cgi-bin/toolkit/file_manager.py?path=' + path;
    spath = path;
    
    breadcrump = spath.split('/');
    $("#bpath").empty()
    allContents=""
    for (var i = 1; i<breadcrump.length - 1; i++) {
        allContents += "/" + breadcrump[i];
        $("#bpath").append("<li><a href='javascript:getContents(\"" + allContents + "\")'>" + breadcrump[i] + "</a></li>");    
    
    }
    
    var currentDir = breadcrump[breadcrump.length - 1];
    var currentPath = allContents + "/" + currentDir;
    $("#bpath").append('<li title="refresh" class="active"><a href="javascript:getContents(\'' + spath + '\')\">' +  currentDir + '</a></li>');    
    
    getJSONResponse(url, displayEntries);

}

function displayEntries(contents) {
    $("#file-manager-table > tbody").html("");

    var table = document.getElementById('file-manager-table');
    
    for (index in contents) {
        entry = contents[index];
        type = 'Other';
        if (entry['type'] == 'd') {
            type = 'Directory';
        }
        else if (entry['type'] == '-') {
            type = 'File';
        }
        var row$ = $('<tr/>');    
        date = entry['date']['day'] + " " + entry['date']['month'];
        if ('year' in entry['date'])
            date += " " + entry['date']['year'];
        else
            date += " " + entry['date']['time'];
        row$.append($('<td/>').html(entry['name']));
        row$.append($('<td/>').html(type));
        row$.append($('<td/>').html(date));
        row$.append($('<td/>').html(entry['owner']));
        row$.append($('<td/>').html(entry['group']));
        row$.append($('<td/>').html(entry['size'] + "B"));
	
        if (type == 'Directory') {
	    var dPath = ''.concat(spath, '/', entry['name']);
	    var bt = $('<button class="btn btn-info"> Calculate </button>');
	    bt.click(function(dPath) {
	    	return function() { redir(dPath); }}(dPath));
	    row$.append($('<td/>').html(bt));
            row$.attr('onclick', "getContents(\"" + spath + "/" + entry['name'] + "\")");
        }
        else if (type == 'File') {
	    row$.append($('<td/>').html(""));
            row$.attr('onclick', "openFile(\"" + spath + "/" + entry['name'] + "\")");
        }
        $("#file-manager-table").append(row$);
    }//for
    
    endProcessing();
    
}
function download(path) {

    window.open('/cgi-bin/toolkit/file_manager.py?download='+path);
}
//------- functions for oppening the dialog
function camelCase(myAwesomeString) {
    myAwesomeString = myAwesomeString.replace(/([^a-zA-Z0-9_\- ])|^[_0-9]+/g, "").trim().toLowerCase();
    myAwesomeString = myAwesomeString.replace(/([ -]+)([a-zA-Z0-9])/g, function(a,b,c) {
        return c.toUpperCase();
    });
    myAwesomeString = myAwesomeString.replace(/([0-9]+)([a-zA-Z])/g, function(a,b,c) {
        return b + c.toUpperCase();
    });
    return myAwesomeString;
}

function getAppIconHtml(appDescrObj){
	return '<a href="javascript:;" class="'+camelCase(appDescrObj['name'])+'link"><img src="../../icons/'+appDescrObj['icon']+'" width="60" height="60"  /></a><a href="javascript:;" class="'+camelCase(appDescrObj['name'])+'link">'+appDescrObj['name']+'</a>'	
}
function setClickFroApp(appDescrObj,path){
	$('a.'+camelCase(appDescrObj['name'])+'link' ).click(function(e){e.preventDefault; appDescrObj['startFunction'].apply(this,[path])});	
	
}
function openBtnsInit(givenApps, path){
	for (var i=0; i<defaultApps.length;i++){
		setClickFroApp(defaultApps[i],path);
	}
	for (a in givenApps){
		setClickFroApp(givenApps[a],path);
	}
	
}
var sharedDialog = null;
function openDialog(givenApps, path){
	//assuming unique names for apps
	var  openDialogHtmlFragments=[]
	for (var i=0; i<defaultApps.length;i++){
		openDialogHtmlFragments.push(getAppIconHtml(defaultApps[i]));
	}
	for (a in givenApps){
		openDialogHtmlFragments.push(getAppIconHtml(givenApps[a]));
	}
	$('#openDialog ul').html('<li>'+openDialogHtmlFragments.join("</li><li>")+'</li>');
	sharedDialog = $( "#openDialog" ).dialog( "open" );
	openBtnsInit(givenApps, path);
}	
function getExtension(path) {
    var i = path.lastIndexOf('.');
    return (i < 0) ? '' : path.substr(i).toLowerCase();
}
function openFile(path) {
	var ext=getExtension(path);
    if (ext!=""){
    	openDialog(extApps[ext], path);
    }else{
    	openDialog({}, path);
    }
        
}

 $(function() {
    $( "#openDialog" ).dialog({
      autoOpen: false,
      show: {
        effect: "fade",
        duration: 1000
      },
      hide: {
        effect: "fade",
        duration: 1000
      }
    });   
  });
