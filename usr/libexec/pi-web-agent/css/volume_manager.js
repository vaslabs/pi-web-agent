
function init() {
    url = '/cgi-bin/toolkit/volume.py';
    getJSONResponse(url, create_controls);
}

function create_controls(data) {
    $( "#slider-vertical" ).slider({
      orientation: "vertical",
      range: "min",
      min: 0,
      max: 100,
      value: data,
      slide: function( event, ui ) {
        $( "#amount" ).val( ui.value );
	url = '/cgi-bin/toolkit/volume.py?update=' + ui.value;
	getJSONResponse(url, handle_vol_update)
	
      }
    });
    $( "#amount" ).val( $( "#slider-vertical" ).slider( "value" ) );
}

function handle_vol_update(data) {
    // data: response from volume update call
    // if error report it

    return 0;
}

$(function() {
    init()
    
});
