var index = 1;
loadedPacks = [];

var Table = document.getElementById("packages-table-id");
if (Table != null)
	Table.innerHTML=""

getPackageResponse( '/cgi-bin/toolkit/package_recommendations.py?index=' + index, loadPackage, index, true );              

//recursive calls to populate the table
function loadPackage( response, index, firstTime ){
  if(!response.hasOwnProperty('STOP')){
    buildHtmlTable( response, firstTime );
    loadedPacks[index] = 1;
    index++;
    if (typeof loadedPacks[index] == 'undefined')
    	getPackageResponse( '/cgi-bin/toolkit/package_recommendations.py?index=' + index, loadPackage, index, false );
  }
}

function getPackageResponse(url, method_call, index, firstTime) {

    var result = null;

    $.ajax({
        url: url,
        type: 'get',
        dataType: 'json',
        async: method_call != null,
        success: function(data) {
            result = data;
            if (method_call != null)
                method_call(result, index, firstTime);    
        } 
    });
    
    //return value;
}

// Builds the HTML Table out of myList.
function buildHtmlTable( myList, firstTime, table_id ) {
    
    if (typeof(table_id) == "undefined") {
        table_id = "packages-table-id"
    }
    var columns = addAllColumnHeaders(firstTime, table_id);
    
    
    for (var i = 0 ; i < myList.length ; i++) {
        var row$ = $('<tr/>');
        var entry = myList[i];
        row$.append($('<td/>').html(entry['Package Name']));
        
        row$.append($('<td/>').html(entry['Status']));
        
        row$.append($('<td/>').html(entry['Description']));
        
        row$.append($('<td/>').html(entry['Version']));
        
        $("#" + table_id).append(row$);
        
    }
    
    if (table_id == 'packages-table-id')
        filter( 'autocomplete', 'packages-table-id' ,1 );
}

// Adds a header row to the table and returns the set of columns.
// Need to do union of keys from all records as some records may not contain
// all records
function addAllColumnHeaders(firstTime, table_id){

    if (typeof(table_id) == "undefined") {
        table_id = "packages-table-id"
    }
    var headerTr$ = $('<tr/>');
    headerTr$.append($('<th/>').html('Package Name'));
    headerTr$.append($('<th/>').html('Status'));
    headerTr$.append($('<th/>').html('Description'));
    headerTr$.append($('<th/>').html('Version'));
    
    
    if(firstTime) {
        $("#" + table_id).prepend(headerTr$);
    }
}

function extensive_search() {
    processing();
    var package_name = $('#autocomplete').val();
    var url="/cgi-bin/toolkit/pm_api.py?op=search&key="+package_name;
    getJSONResponse(url, renderSearchResults);
}

function renderSearchResults(data) {
    pkg_list = [];
    $('#packages-table-id').css('display', 'none');
    $('#packages-table-id').parent().append('<div id="searched_packages_table"></div>');
    $('#searched_packages_table').html('<table id="searched_packages_table_id"></table>');
       
    $.each(data, function (key, value) {
        var pkg = [];
        pkg['Package Name'] = key;
        pkg['Description'] = value;
        pkg['Version'] = 'N/A'
        var status$='<div/>';
        status$ = $(status$).attr('id', key);
        status$ = $(status$).attr('class', 'install-status');
        status$ = $(status$).html('<div class="progress progress-striped active"><div class="progress-bar progress-bar-info " style="width: 100%"></div></div>');
        pkg['Status'] = status$;
        pkg_list.push(pkg);
        
    });
    
    buildHtmlTable( pkg_list, true, 'searched_packages_table_id')
    $(".form-group #autocomplete").css('display', 'none');
    $(".form-group #extensive_search").css('display', 'none');
    $(".form-group").append('<button id="go_back_button" class="btn btn-primary" onclick="go_back()">Back to recommended packages</button>');
    endProcessing();
    findPackageInstallationStatus(Object.keys(data));
}

function findPackageInstallationStatus(keys) {
    var url="/cgi-bin/toolkit/pm_api.py?op=check_group&packages="+JSON.stringify(keys);
    getJSONResponse(url, renderInstallationTextBoxes);
}

function renderInstallationTextBoxes(data) {
    $.each(data, function (key, value) {
        var checkbox = value['content'][0];
        $('#' + key + '.install-status').html(checkbox);
    });
}

function go_back() {
    $('#searched_packages_table').remove();
    $('#packages-table-id').css('display', 'block');
    $(".form-group #autocomplete").css('display', 'block');
    $(".form-group #extensive_search").css('display', 'block');
    
    $(".form-group #autocomplete").val("");
    $(".form-group #autocomplete").trigger('change');
    $('#go_back_button').remove();
}
