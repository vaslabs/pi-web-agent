function update_res(res) {
    var dpkg_config_needed = 200;
    var message = '';
    if (res.status == dpkg_config_needed) {
	message = '<br><h4>Warning: Last update was interrupted!</h4>\
                  <br><h5>Recovery procedure initiated. Please come back in a moment...</h5>';
    } else {
	message = '<br><h4>Update procedure initiated!</h4> Please come back in a moment...';
    }

    $("#extension-main-view").html(message);
    endProcessing();
}

function do_update() {
    url = '/cgi-bin/toolkit/update_api.py?op=update';
    processing();
    getJSONResponse(url, update_res);
}

function no_action_msg() {
    $("#extension-main-view").html('<br><h4>System is up to date!</h4>');
    var bt = $('<button type="button" onClick="check_update()" class="btn btn-success">Check</button>');
    $("#extension-main-view").append(bt);
    
}

function new_update_msg() {
    $("#extension-main-view").html('<br><h4>Warning: Last update was interrupted!</h4>\
                                    <br><h5>Recovery procedure initiated. \
                                    Please come back in a moment...</h5>');
}

function reboot_required_msg() {
    $("#extension-main-view").html('<br>Reboot is required to apply previous updates.');
}

function update_pending_msg() {
    $("#extension-main-view").html('<br>Update in progress. Please try again later...');
}

function interrupted_msg() {
    $("#extension-main-view").html('<br><h4>Warning: Last update was interrupted!</h4>\
                                    <br><h5>Recovery procedure initiated.\
                                    Please come back in a moment...</h5>');
}

function display_packages(res) {
    var status = {0: no_action_msg,
		  101: no_action_msg,
		  120:reboot_required_msg,
		  100:update_pending_msg
		 };

    if (status[res.status]) {
	status[res.status]();
	endProcessing();
	return;
    }

    if (res.status != 110) {
	interrupted_msg();
	endProcessing();
	return;
    }
    
    var n_packages = res.package_list.length;
    for (var i=0; i<n_packages; i++) {
	//build the table here
	var pack = res.package_list[i];
	var row$ = $('<tr/>');
	row$.append($('<td/>').html(pack.package_name));
	row$.append($('<td/>').html(pack.description));
	$("#update-table").append(row$);	    
    }

    //make table and update button visible
    $('#update-table').show();
    $('#update-button').show();
    endProcessing();
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
	$("#extension-main-view").html('The Update Manager is busy right now. \
                                       This page will automatically reload once\
                                       the service is available');
	getResponse('/cgi-bin/toolkit/live_info.py?cmd=apt', checkAptBusy);
	endProcessing();
    } else {
	get_packages();
    }

}


function init() {
    $('#update-table').hide();
    $('#update-button').hide();
    $('#update-button').click(do_update);
    url = '/cgi-bin/toolkit/update_api.py?op=get_status';

    processing();
    getJSONResponse(url, main);
}

$(function(){
    init();
}); 
