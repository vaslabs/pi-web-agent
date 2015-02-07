
function no_action_msg() {
    $("#extension-main-view").html('');
}

function new_update_msg() {
    $("#extension-main-view").html('Yo');
}

function reboot_required_msg() {
    $("#extension-main-view").html('');
}

function update_pending_msg() {
    $("#extension-main-view").html('');
}


function display_packages(res) {
    var status = {0: no_action_msg,
		  101: no_action_msg,
		  110: new_update_msg,
		  120:reboot_required_msg,
		  100:update_pending_msg
		 };

    if (status[res.status]) {
	status[res.status]();
	endProcessing();
	return;
    }

    for (pack in res.packages) {
	//build the table here
    }

    //make table and update button visible
    $('#update-table').show();
    $('#update-button').show();
}

function get_packages() {
    url = '/cgi-bin/toolkit/update_api.py?op=get_packages';
    getJSONResponse(url, display_packages);
}


function checkAptBusy(response){
     if (response == 'True')
        setTimeout(function() {getResponse('/cgi-bin/toolkit/live_info.py?cmd=apt',
                    checkAptBusy)}, 5000); 
    else
        navigate('/cgi-bin/toolkit/package_recommendations.py?type=js');
}

function main(res) {
    if (res.status == "busy") {
	$("#extension-main-view").html('The Update Manager is busy right now. This page will automatically reload once the service is available');
	getResponse('/cgi-bin/toolkit/live_info.py?cmd=apt', checkAptBusy);
	endProcessing();
    } else {
	get_packages();
    }

}


function init() {
    $('#update-table').hide();
    $('#update-button').hide();
    url = '/cgi-bin/toolkit/update_api.py?op=get_packages';

    processing();
    getJSONResponse(url, main);
}

$(function(){
    init();
}); 
