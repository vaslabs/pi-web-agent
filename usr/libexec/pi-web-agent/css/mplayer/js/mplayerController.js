/**
* The object that controls how ui is 
* controlled eg.by 3d party updates.
*as only one controller is needed
*I have decided to go for a 
*singleton here.(using closure)
*/
var mplayerController= (function () {
	  var instance;
	  function init(volEl) {
	 
	    /**
	    * volume's numeric value
	    * 
	    * @property volume
	    * @type {Number}
	    * @default null
	    */
	    var volume, 
	    /**
	    * Master volume's jquery object
	    * @property volEl
	    * @type {Object}
	    * @default null
	    */
	    volumeEl=volEl,
	    /**
	    * Tasks denotes tasks cancelled
	    * when zero execute the tasks given
	    * to the execute function
	    * @property tasks
	    * @type {Number}
	    * @default 0
	    */
	    tasks=0;
	    function getVolumeFromSlaveProtocolReply(str){
	    	if (isNaN(str)){
	    		var parts=str.split(":");
		    	if (parts.length<2){
		    		  throw{
		    			  name: "SlaveProtocolStringError",
		    			  message: "Invalid slave protocol string."
		    			 };
		    	}
		    	return parseInt(parts[1]);
	    	}
	    	return parseInt(str)
	    }
	    
	    return {

	    	/*set volume accepts number
	    	 * or string in the format returned by mplayer
	    	 * it also locks the player from sending back
	    	 * the update to avoid a non terminating 
	    	 * loop of messages
	    	 */
			setVolume: function(vol) {
				vol=getVolumeFromSlaveProtocolReply(vol)
				tasks++;
				volumeEl.val(vol);
				volume=vol;
			},execute:function(cb){
				if(tasks==0&&typeof cb=="function"){
					return cb();
				}
				tasks--;
				
			}
	    };
	 
	  };
	 
	  return {
	 
	    // Get the instance if one exists
	    // or create one if it doesn't
		//only accespts elementson first call
	    getInstance: function (volumeEl) {
	 
	      if ( !instance ) {
	    	  if (!volumeEl || !volumeEl instanceof jQuery){
	    		  throw{
	    			  name: "VolumeElementError",
	    			  message: "No a valid jquery element!"
	    			 };
	    	  }
	    	  instance = init(volumeEl);
	      }
	 
	      return instance;
	    }
	 
	  };
	 
	})();
	 
