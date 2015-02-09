/**
* The object that controls is responsible
* for end to end connectivity to mplayer(not just websocketd)
* on startConnectonCheck a request is send to the server
* if there is no reply in "sensitivity" amount of  milliseconds
* the callback of startConnectonCheck gets called, otherwise
* the endConnection check should be called  to stop the 
* connection check procedure as the client has verified
* successful communication, timeout gets cleared and nothing
* gets executed.
*/
/*only one instance of the connectionChecker is needed*/
var connectionChecker= (function () {
	  var instance;
	  function init(sensitivity) {
		var timer
		//sensitivity in milliseconds
		, sensitivity=sensitivity;
	    return {

	    	/*
	    	 *Starts connection check
	    	 */
	    	startConnectionCheck:function(cb){
	    		timer.setTimeout(function(){
	    			if(typeof cb==="function"){
	    			 cb();
	    			}
	    		},sensitivity);
	    	},
	    	endConnectionCheck:function(){
	    		clearTimeout(timer);
	    	}
	    };
	 
	  };
	 
	  return {
	 
	    // Get the instance if one exists
	    // or create one if it doesn't
	    getInstance: function (sensitivity) {
	 
	      if ( !instance ) {
	    	  instance = init(sensitivity);
	      }
	 
	      return instance;
	    }
	 
	  };
	 
	})();

