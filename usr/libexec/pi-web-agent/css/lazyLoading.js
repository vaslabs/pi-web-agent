var index = 1;
getPackageResponse( '/cgi-bin/toolkit/package_recommendations.py?index=' + index, loadPackage, index, true );
              
function loadPackage( response, index, firstTime ){
  if(!response.hasOwnProperty('STOP')){
    buildHtmlTable( response, firstTime );
    index++;
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
        for (var colIndex = 0 ; colIndex < columns.length ; colIndex++) {
          var cellValue = myList[i][columns[colIndex]];

          if (cellValue == null) { cellValue = ""; }

          row$.append($('<td/>').html(cellValue));
        }
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
        for (var key in rowHash) {
            if ($.inArray(key, columnSet) == -1){
                columnSet.push(key);
                headerTr$.append($('<th/>').html(key));
            }
        }
    }
    if(firstTime)
      $("#packages-table-id").append(headerTr$);

    return columnSet;
}   
