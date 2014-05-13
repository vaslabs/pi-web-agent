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
function filter ( _input_id, _table_id, cellNr){
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


/*
var textContentProp = "innerText" in document.body ? "innerText" : "textContent";
function updateView(){
  var table = document.getElementById("packages-table-id");
  var ui = document.getElementById("ui-id-1");
  var li = ui.getElementsByTagName("li");

  var suggestionList = [];

  for (var i=0; i < li.length; i++) {
    //alert( li[i].innerHTML );
    alert( li[i][textContentProp] );
    suggestionList.push( li[i][textContentProp] );
  }

  $.ajax({
      url: '/cgi-bin/toolkit/package_recommendations.py?action=updatePackageListView',
      type: 'get',
      dataType: 'json',
      async: true,
      success: function(data) {
        for( var key in data ){
          alert( key );
        }

      //iterate in data and get rid of the missing packages depending on what's in the suggestion list.
 //     buildHtmlTable( response, firstTime );
      } 
  });

}


function getText()
{
    return document.getElementById('menu_selected')[textContentProp];
}
*/

