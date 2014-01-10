spath='/home';
getContents('/home')

function getContents(path) {
    url = '/cgi-bin/toolkit/file_manager.py?path=' + path;
    spath = path;
    
    breadcrump = spath.split('/');
    $("#bpath").empty()
    allContents=""
    for (var i = 1; i<breadcrump.length - 1; i++) {
        allContents += "/" + breadcrump[i];
        $("#bpath").append("<li><a href='javascript:getContents(\"" + allContents + "\")'>" + breadcrump[i] + "</a></li>");    
    
    }
    
    $("#bpath").append("<li class=\"active\">" +  breadcrump[breadcrump.length - 1] + "</li>");    
    
    $(".span16").prepend(animationBar());
        
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
            row$.attr('onclick', "getContents(\"" + spath + "/" + entry['name'] + "\")");
        }
        else if (type == 'File') {
            row$.attr('onclick', "openFile(\"" + spath + "/" + entry['name'] + "\")");
        }
        $("#file-manager-table").append(row$);
    }//for
    $("#b-pb").remove()
}
//------- functions for oppening the dialog
function camelCase(myAwesomeSring) { 
    return myAwesomeSring.toLowerCase().replace(/-(.)/g, function(match, group1) {
        return group1.toUpperCase();
    });
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
	$( "#openDialog" ).dialog( "open" );
	openBtnsInit(givenApps, path);
	//console.log(JSON.stringify($('#openDialog').html()));
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