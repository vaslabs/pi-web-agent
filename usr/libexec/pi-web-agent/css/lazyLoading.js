var index = 1;
loadedPacks = [];

var Table = document.getElementById("packages-table-id");
if (Table != null)
	Table.innerHTML=""

getPackageResponse( '/cgi-bin/toolkit/package_recommendations.py?index=' + index, loadPackage, index, true );              

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
                method_call(result,index, firstTime);    
        } 
    });
    
    //return value;
}

// Builds the HTML Table out of myList.
function buildHtmlTable( myList, firstTime ) {
    var columns = addAllColumnHeaders(myList, firstTime);
    for (var i = 0 ; i < myList.length ; i++) {
        var row$ = $('<tr/>');
        var entry = myList[i];
        row$.append($('<td/>').html(entry['Package Name']));
        
        row$.append($('<td/>').html(entry['Status']));
        
        row$.append($('<td/>').html(entry['Description']));
        
        row$.append($('<td/>').html(entry['Version']));
        $("#packages-table-id").append(row$);
        
    }
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
