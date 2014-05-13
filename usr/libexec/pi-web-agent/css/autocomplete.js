$(function() {
  var availableTags = [];
  var currentAvailableTags = [];

  $.ajax({
      url: '/cgi-bin/toolkit/package_recommendations.py?action=getPackageList',
      type: 'get',
      dataType: 'json',
      async: true,
      success: function(data) {
        for (var i = 0 ; i < data.length ; i++) {
          availableTags.push(data[i]['label']);
        }
      } 
  });

  //added regex to much the start of each package name
  $( "#autocomplete" ).autocomplete({
  source: function( request, response ) {
      var matcher = new RegExp( "^" + $.ui.autocomplete.escapeRegex( request.term ), "i" );
      response( $.grep( availableTags, function( item ){
        return matcher.test( item );
      }) );
    }
  
  });
});

var textContentProp = "innerText" in document.body ? "innerText" : "textContent";
// filters the table depending on the text in the search box after a keystroke
// or when a new row is added in the table
function filter ( _input_id, _table_id, cellNr ){
  if( document.getElementById( _input_id ) != null ){  
    var inputValue = document.getElementById( _input_id ).value.toLowerCase();
    var table = document.getElementById(_table_id);
    var ele;
    for (var r = 1; r < table.rows.length; r++){
  //	  alert( table.rows[r][textContentProp]);
	    ele = table.rows[r][textContentProp];
	    if (ele.toLowerCase().indexOf( inputValue )>=0 )
		    table.rows[r].style.display = '';
	    else table.rows[r].style.display = 'none';
	  }
	}
}
