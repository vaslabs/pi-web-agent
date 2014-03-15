setInterval(function(){
  if( getAptResponse('/cgi-bin/toolkit/live_info.py?cmd=apt') == 'False' ){
    location.reload(false);
  }
},5000);

function getAptResponse(url) {

    var result = null;

    $.ajax({
        url: url,
        type: 'get',
        dataType: 'xml',
        async: true,
        success: function(data) {
            result = data;
            var xmlDoc = result,
            $xml = $( xmlDoc ),
            $title = $xml.find("response");
            value = $title.text();
        } 
    });
    
    return value;
}
