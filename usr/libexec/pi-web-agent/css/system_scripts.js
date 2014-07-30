function navigate(link) {
     $(".span16").html('');
     processing();
     $(".span16").load(link);
      window.history.pushState({}, "", link.split("?")[0]);
}

function animationBar() {
    return '<div id="b-pb" class="progress progress-striped active"><div class="progress-bar" style="width: 100%"></div></div>'
}

function check_for_updates() {
    processing();
    $("#check_button").remove()
    getJSONResponse('/cgi-bin/toolkit/live_info.py?cmd=check_app', update_check_completed) 
}

function update_app() {
    processing();
    $("#update_button").remove();    
    getResponse('/cgi-bin/toolkit/live_info.py?cmd=update_app', update_response);
}

function processing() {
    $('.progress.progress-striped.active').remove();
    $(".span16").prepend(animationBar());
}

function endProcessing() {
    $("#b-pb").remove();
}

function update_response(response) {
    if (response == "0")
        check_for_updates();
    else
        $("#updates").append('Update failed. Please try again later');
    endProcessing();
}
function update_check_completed(info) {
    
    if ('code' in info && info['code'] == 0) {
        $("#updates").append('Application is in its latest version');
    }
    else {
        $("#updates").append('Version: ' + info['tag_name'] + '<br>');
        $("#updates").append(info['body'].replace(/\n/g,"<br>") + '<br><br>');
        $("#updates").append('<button class="btn btn-info" type="button" onclick="update_app()" id="update_button">Update</button>');
    }
    endProcessing();

}

function start_live_streaming() {
    getResponse('/cgi-bin/toolkit/camera.py?cmd=start', sls)
}

function sls(info) {
    return;
}

function stop_live_streaming() {
    getResponse('/cgi-bin/toolkit/camera.py?cmd=stop', sls)
}

// Builds the HTML Table out of myList.
function buildHtmlTableFromObject( obj, tableID, keys) {

    $.each(Object.keys(obj), function () {
        var row$ = $('<tr/>');
        row$.append($('<td/>').html(this));
        var entry = obj[this];
        $.each(keys, function() {
            row$.append($('<td/>').html(entry[this]));
        });
        
        $("#" + tableID).append(row$);
        
    });
}


// Adds a header row to the table and returns the set of columns.
// Need to do union of keys from all records as some records may not contain
// all records
function addAllColumnHeaders(myList, firstTime){

    var columnSet = [];
    var headerTr$ = $('<tr/>');

    for (var i = 0 ; i < myList.length ; i++) {
        var rowHash = myList[i];
        columnSet.push('Package Name');
        headerTr$.append($('<th/>').html('Package Name'));
        columnSet.push('Status');
        headerTr$.append($('<th/>').html('Status'));
        columnSet.push('Description');
        headerTr$.append($('<th/>').html('Description'));
        columnSet.push('Version');
        headerTr$.append($('<th/>').html('Version'));
        
    }
    if(firstTime)
      $("#packages-table-id").prepend(headerTr$);

    return columnSet;
}   

function addColumnHeadersToTable(tableID, headers){

    var columnSet = [];
    var headerTr$ = $('<tr/>');

    for (var i = 0 ; i < headers.length ; i++) {
        columnSet.push(headers[i]);
        headerTr$.append($('<th/>').html(headers[i]));
    }
    $("#" + tableID).prepend(headerTr$);
}

function showDialog(dtitle, content) {

    $("#dialog").dialog({title: dtitle, width: "75%"});
    $("#dialog_content").html('');
    $("#dialog_content").html(content);
}

function closeDialog() {
    $("#dialog").dialog('close');
}

function popSuccessMessage(msg) {
    var dialog = '<div class="alert alert-dismissable alert-success"><button type="button" class="close" data-dismiss="alert">×</button>' +
              '<strong>Success</strong>' + msg + '.</div>'
    $(".span16").prepend(dialog);
}


function popFailMessage(msg) {
    var dialog = '<div class="alert alert-dismissable alert-danger"><button type="button" class="close" data-dismiss="alert">×</button>' +
              '<strong>Failed: </strong>' + msg + '.</div>'
    $(".span16").prepend(dialog);
}
