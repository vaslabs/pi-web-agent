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
            row$.attr('onclick', "download(\"" + spath + "/" + entry['name'] + "\")");
        }
        $("#file-manager-table").append(row$);
    }//for
    $("#b-pb").remove()
}

function download(path) {

    window.location='/cgi-bin/toolkit/file_manager.py?download='+path;

}
