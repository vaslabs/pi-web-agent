getResponse('/cgi-bin/toolkit/live_info.py?cmd=apt', checkAptBusy);
    

function checkAptBusy(response){

     if (response == 'True')
        setTimeout(function() {getResponse('/cgi-bin/toolkit/live_info.py?cmd=apt',
                    checkAptBusy)}, 5000); 
    else
        navigate('https://raspberrypi:8003/cgi-bin/toolkit/package_recommendations.py?type=js');
}

