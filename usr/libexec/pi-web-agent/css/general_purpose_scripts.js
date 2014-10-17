$(function(){
    initialise();
    
});

function enableProtocolRule() {
    if($("#enableProtocolCheckBox").is(':checked'))
        $("#selectProtocol").show();  // checked
    else
        $("#selectProtocol").hide();  // unchecked
}

function enableIPRule() {
    if($("#enableIPCheckBox").is(':checked'))
        $("#ipAddress").show();  // checked
    else
        $("#ipAddress").hide();  // unchecked
}

function getMemoryInfo(usage) {
     //stab TODO
     //var usage =   Math.floor((Math.random()*100));
     var msg = "Mem usage: " + Math.round(usage*100) + "%";
     html = generateCriticalMessage(usage, msg);  
     $('#li_memory').html(html);
    
    
}

function check_started(response) {
    location.reload(false);
}
    
function check_update() {
    getResponse('/cgi-bin/toolkit/live_info.py?cmd=check', check_started)
}

function getTempInfo(temp) {
    //stab TODO
    //var usage =   Math.floor((Math.random()*100));
    var msg = "Temperature: " + Math.round(temp);
    if (temp == 'N/A')
        html = generateCriticalMessage(86, msg);        
    else if (temp > 65)    
        html = generateCriticalMessage(99, msg + "'C");
    else if (temp > 55)
        html = generateCriticalMessage(86, msg + "'C");
    else 
        html = generateCriticalMessage(10, msg + "'C");  
    $('#li_temp').html(html);
}

function getSwapInfo(usage) {
    //stab TODO
     //var usage =   Math.floor((Math.random()*100));
     var usg = 0;
     if (usage > 0) {
        usg=usage*10;
     }
     var msg = "Swap usage: " + Math.round(usage*100) + "%";
     if (usage < 0) {
        msg = "No swap space";
        usg=0;
     }
     html = generateCriticalMessage(usg, msg);  
     $('#li_swap').html(html);
    
}
function getHardDiskInfo(usage) {
    //stab TODO
    //var usage =   Math.floor((Math.random()*100)); 
    var msg = "Disk usage: " + Math.round(usage*100) + "%";
    html = generateCriticalMessage(usage, msg); 
    $('#li_hard_drive').html(html);
}

function getUpdateCheck(info) {
    var html = ''
    if (info == true)
    {
        html = generateCriticalMessage(86, "Updates available");
    }
    else
        html = generateCriticalMessage(0, "System is up to date");

    $('#li_update').html(html);
}


function generateCriticalMessage(usage, msg) {

    var span = "label label-success";
    if (usage >= 95)
    {
        span = "label label-danger";
    }
    else if (usage >= 85) {
        span="label label-warning";
    }
    var html = '<span class="'+span+'">' + msg +
    '</span>';
    return html; 
}

function getResponse(url, method_call) {

    var result = null;

    $.ajax({
        url: url,
        type: 'get',
        dataType: 'xml',
        async: method_call != null,
        success: function(data) {
            result = data;
            var xmlDoc = result,
            $xml = $( xmlDoc ),
            $title = $xml.find("response");
                value = $title.text();
            if (method_call != null)
                method_call(value);    
        } 
    });
    
    //return value;
}
 
 
function getJSONResponse(jsurl, method_call) {

    var result = null;

    $.ajax({
        url: jsurl,
        cache: false,
        type: 'get',
        dataType: 'json',
        async: method_call != null,
        success: function(data) {
            if (method_call != null)
                method_call(data);
            else 
                result = data;    
        } 
    });
    
    return result;
} 

function getKernelInfo(info) {
    //stab TODO
    var html='<span class="label label-info">\nKernel: <br>\n'+
    info+'\n</span>\n';
    $('#li_kernel').html(html);
    
}   
    
function getHostnameInfo(info) {
    //stab TODO

    html='<span class="label label-info">\nHostname: <br>'+
    info+'\n</span>\n';
    $('#li_hostname').html(html);
}

function initialise()
{
    getMemoryInfo('...');
    getStatuses();
}

function getStatuses() {
    url = '/cgi-bin/toolkit/live_info.pwa'
    getJSONResponse(url, updateStatuses);
}

function updateStatuses(statuses) {
    getHostnameInfo(statuses['ip']['address']);
    getKernelInfo(statuses['kernel']);
    getUpdateCheck(statuses['ucheck']);
    getTempInfo(statuses['temp']);
    getMemoryInfo(statuses['mem']);
    getHardDiskInfo(statuses['disk']);
    getSwapInfo(statuses['swap']);
    setTimeout(getStatuses, 800);
}

function submit_package(element) {
    var url='/cgi-bin/toolkit/installUninstallPackage.py?packageName='+element.name+'&action=';
    
    var param2='install';
    if (element.checked)
    {
       param2='uninstall';
    }
    url+= param2;   
    var info=getResponse(url);

    $('#packages-table').text("Installation in progress. . .The page will reload in 3 seconds:");    
    reloadInXSecs( 3000 );
}

function reloadInXSecs( secs ){
  setTimeout(function () { location.reload(1); }, secs);
}

function getPackageResponse(url) {
    var value = -1;

    $.ajax({
        type: "GET",
        url: url,
        async: false,
        success : function(data) {
            result = data;
            var xmlDoc = result,
            $xml = $( xmlDoc ),
            $title = $xml.find("response");
            value = $title.text();
                
        }
    });

    return remote;
    
    //return value;
}

function camera_utils(action) {

        
    var url='/cgi-bin/toolkit/camera_utils.py?action='+action;
    if (action == "snapshot") {
        $(".span16").prepend(animationBar());
        getJSONResponse(url, displaySnapshot);
        return;
    }
    var info=getResponse(url, null);
}

