//helpers
function showAppropriateView(){
	 $("#mplayerPlayView").hide();
	 $("#mplayerLauncherView").hide();
	$("#mplayerLoader").show();                
	$.getJSON( "mplayer_api.py", function( data ) {
	if (data.status=="playing") {
		// data.redirect is the redirection link
        $("#mplayerPlayView").show();
		updateStatus(data)
		if (!mplayerSock){
                            mplayerSock=mplayerWebSocket();
		}
		console.log("loader hidden");
	}
	else {
                        
                            $("#mplayerLauncherView").show();
	}
	$("#mplayerLoader").hide();
	});

	
}
function constructInitObject(formArr){
    var initObj={}
    for (var i=0; i<formArr.length;i++){
        initObj[formArr[i]["name"]]=formArr[i]["value"];
    }
    return {init:initObj};
}
function updateStatus(data){
	$("#status").html(data.status);
}
function showInfo(info){
	$("#status").html(info);
}
//globals
window.volume= 20;
window.eqvals=[0,0,0,0,0,0,0,0,0,0];   
var mplayerSock;
var volElements=$("#master,#volume")
var controller=mplayerController.getInstance(volElements)
//ui
$(function() {
	// setup master volume
	$('#master').knob({
	    'release' : function (v) {
	    	console.log('release1');
	    	controller.execute(function(){
	    		console.log('release2');
	    		$.post( "mplayer_api.py", JSON.stringify({ volume: v, eqhelper: window.eqvals}));
	    		});
			}
	});
	$('#volume').knob();
	//start stream button
	$("#startStreamBtn").click(function(event){
	    //alert(JSON.stringify(constructInitObject($('#launcherForm').serializeArray())))
		$(".mplayerView").hide();
		$("#mplayerLoader").show();  
		$.post( "mplayer_api.py", JSON.stringify(constructInitObject($('#launcherForm').serializeArray())))
				.done(function( data ) {
	                                if (data.status=="starting"){
	                                    
	                                    mplayerSock=mplayerWebSocket();
	                                }
	                                    updateStatus(data)
	                                
	                                
				});
	});
    $("#radio label").click(function(){
        $("[name=output]").val($(this).text());

    });


    $( "#radio" ).buttonset();
    ///setup circular view eq knobs
    /* Apply a class to each child
    * Required for IE8-
    */
   $('.circle-container').children().each(function() {
     $(this).addClass('item'+($(this).index() + 1));
   });
   $('.eq').prop("value",0)
             .data("fgColor","#999999")
             .data("width",100)
             .data("height",100)
             .data("thickness",0.7)


   $('.eq').knob({ "min":-12,
	               "max":12,
	               "fgColor":"#999999",
	               "skin":"tron",
	               "release" : function (v) {
	            	   window.eqvals=[]; 	
		       		   $( ".eq" ).each(function(index,element) { 	
		       				window.eqvals.push(parseInt($(this).val())); 	
		       		   } );
		       		   $.post( "mplayer_api.py", JSON.stringify({ eq: window.eqvals, volumehelper: parseInt($("#").val()) }))
		       			.done(function( data ) {
		       				updateStatus(data)
		       		   });
		       		}
   				});

});

$(document).ready(function(){
	
	showAppropriateView();

});

function mplayerWebSocket(){
	try{
		var ws = new ReconnectingWebSocket('wss://'+window.location.hostname+':7777');
	}catch(e){
		window.open('https://'+window.location.hostname+':7777', '_blank');
		updateStatus({status:'please add exception and refresh'});
		$("#mplayerLauncherView").show();
	}
    ws.onopen = function() {
    	$("#mplayerLoader").hide(); 
            $(".mplayerView").hide();
            $("#mplayerPlayView").show();
            
    updateStatus({status:'CONNECTED'});

  };
   ws.onclose = function() {
    updateStatus({status:'DISCONNECTED'});
  };
   ws.onmessage = function(event) {
	   console.log("message:"+event.data)
	   if (event.data.indexOf("volume") > -1){
		   controller.setVolume(event.data); 
	   }
    showInfo(event.data);
  };
  return ws
  

}