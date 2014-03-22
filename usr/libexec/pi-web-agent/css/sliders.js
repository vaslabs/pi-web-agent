function updateStatus(data){
	$("#status").html(data.status);
}
$(function() {
// setup master volume
	
// setup graphic EQ
$( "#eq > span" ).each(function() {
	// read initial values from markup and replace them with equalizer 
	var value = parseInt( $( this ).text(), 10 );
	$( this ).empty().slider({
		min : -12,
		max : 12,
		value: value,
		range: "min",
		animate: true,
		orientation: "vertical",
		stop: function(event, ui) {
			window.eqvals=[];
			$( "#eq > span" ).each(function(index,element) {
				window.eqvals.push($(element).slider("value"));
			} );
			$.post( "mplayer_status.py", JSON.stringify({ eq: window.eqvals, volumehelper: $("#master").slider("value")  }))
			.done(function( data ) {
				updateStatus(data)
			});
		}
	});
});
$( "#master" ).slider({
		value: window.volume,
		orientation: "horizontal",
		range: "min",
		animate: true,
		stop: function(event, ui) {
			$.post( "mplayer_status.py", JSON.stringify({ volume: ui.value, eqhelper: window.eqvals}))
			.done(function( data ) {
				updateStatus(data)
			});
	}
});
});