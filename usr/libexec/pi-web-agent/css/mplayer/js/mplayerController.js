/**
* The object that controls how ui is 
* controlled eg.by 3d party updates.
*as only one controller is needed
*I have decided to go for a 
*singleton here.(using closure)
*/
/*in the next version with the new api 
all requests used by mplayer_controls 
ui will go here*/
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
	    volumeEl=volEl;
	    function getVolumeFromSlaveProtocolReply(str){
	    	if (isNaN(str)){
	    		var parts=str.split("=");
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
				vol=getVolumeFromSlaveProtocolReply(vol);
				volumeEl.val(vol);
				volumeEl.trigger('change')
				volume=vol;
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
	 
