$(document).ready(function(){
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
     var msg = "Mem usage: " + usage + "%";
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
    var msg = "Temperature: " + temp;
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
     var msg = "Swap usage: " + usage + "%";
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
    var msg = "Disk usage: " + usage + "%";
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
 
 
function getJSONResponse(url, method_call) {

    var result = null;

    $.ajax({
        url: url,
        type: 'get',
        dataType: 'json',
        async: method_call != null,
        success: function(data) {
            if (method_call != null)
                method_call(data);    
        } 
    });
    
    //return value;
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
    url = '/cgi-bin/toolkit/live_info.py?cmd=all_status'
    getJSONResponse(url, updateStatuses);
}

function updateStatuses(statuses) {
    getHostnameInfo(statuses['hostname']);
    getKernelInfo(statuses['kernel']);
    getUpdateCheck(statuses['ucheck']);
    getTempInfo(statuses['temp']);
    getMemoryInfo(statuses['mem']);
    getHardDiskInfo(statuses['disk']);
    getSwapInfo(statuses['swap']);
    setTimeout(getStatuses, 8000);
}

function submit_function(element) {
    
     var url='/cgi-bin/toolkit/live_info.py?cmd=edit_service&param1='+element.id;
     var param2='off';
     if (element.checked)
     {
        param2='on';
     }
     url+='&param2=' + param2;   
     var info=getResponse(url, null);
}

function submit_gpio_direction(element) {
     
     var url='/cgi-bin/toolkit/onOffPin.py?id='+element.id+'&pinNumber='+element.name+'&direction='
     var direction='in';
     if (element.attributes["direction"].value=="IN")
     {
        direction='out';
     }
     url+=direction+"&from="+element.attributes["direction"].value
     var info=getResponse(url, null);

}

function submit_gpio_value(element) {
     
     var url='/cgi-bin/toolkit/onOffPin.py?id='+element.id+'&pinNumber='+element.name+'&value='
     var value='0';
     if (element.checked)
     {
        value='1';
     }
     url+=value
     var info=getResponse(url, null);
}
function gpio_clear() {
    var url='/cgi-bin/toolkit/onOffPin.py?cmd=cleanup'
    var value='0';
    var info=getResponse(url, null);
    result = info;
    var xmlDoc = result,
    $xml = $( xmlDoc ),
    $title = $xml.find("response");
    value = $title.text();
    if (value == 0) {
        html_message = '<div class="success" id="user_message">Successful clean up</div>';
    } 
    else {
        html_message = '<div class="error" id="user_message">Cleanup failed</div>';
    }
    $('#gpio_table').remove();
    $('#user_space').prepend(html_message);
    setTimeout(function() { location.reload(); }, 1000);
    
}

function open_iptables_panel(chain_name) {

    $("#ip_overlay").overlay({
     
        // custom top position
        top: 260,

        // some mask tweaks suitable for facebox-looking dialogs
        mask: {

            // you might also consider a "transparent" color for the mask
            color: '#fff',

            // load mask a little faster
            loadSpeed: 200,

            // very transparent
            opacity: 0.5
        },

        // disable this for modal dialog-type of overlays
        closeOnClick: false,

        // load it immediately after the construction
        load: true

    });

    var rules_overlay = document.getElementById("ip_overlay");
    rules_overlay.setAttribute("name", chain_name);
    $("#selectProtocol").hide();
    $("#ipAddress").hide();
}

function validateIPField() {
    if (!document.getElementById("enableIPCheckBox").checked) {
        submitProtocolRule();
        return;
    }
    var ipAddressElement = document.getElementById("ipAddress").value;
    var letters = /^[0-9a-zA-Z.]+$/;
    if (ipAddressElement.match(letters))
        submitProtocolRule();
    else {
        alert("This is not a valid source address!");
    }
}

function submitProtocolRule(){
    $("#addRuleID").submit(function(){
        var protocolChecked = document.getElementById("enableProtocolCheckBox").checked;
        var ipaddressChecked = document.getElementById("enableIPCheckBox").checked;
        var chainElement = document.getElementById("ip_overlay");
        var chain = chainElement.getAttribute("name");
        var actionElement = document.getElementById("selectAction");
        var action = actionElement.options[actionElement.selectedIndex].text;        
        if (protocolChecked && !ipaddressChecked) {        
            var protocolElement = document.getElementById("selectProtocol");
            var protocol = protocolElement.options[protocolElement.selectedIndex].text;
            getIPTableValues(chain, action, protocol, "None");
        }
        else if (ipaddressChecked && !protocolChecked) {
            var ipAddressElement = document.getElementById("ipAddress").value;
            getIPTableValues( chain, action, "None", ipAddressElement);
        }
        else if (ipaddressChecked && protocolChecked){
            var protocolElement = document.getElementById("selectProtocol");
            var protocol = protocolElement.options[protocolElement.selectedIndex].text;
            var ipAddressElement = document.getElementById("ipAddress").value;
            getIPTableValues(chain, action, protocol, ipAddressElement);
        }
    });
}

function getIPTableValues(chain, action, protocol, ip_address) {
    var remote;
    var url='/cgi-bin/toolkit/add_iptable_rules.py?chain='+chain+'&action='+action+'&protocol='+protocol+'&ipaddress='+ip_address;
    $.ajax({
        type: "GET",
        url: url,
        async: false,
        success : function(data) {
            remote = data;
        }
    });
    return remote;
    
    //return value;
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

function toggleOverlay(){
//    open_iptables_panel('12')
    var overlay = $('#ip_overlay');
    overlay.style.opacity = .8;
    if(overlay.style.display == "block"){
        overlay.style.display = "none";
        location.reload(false)
    } else {
        overlay.style.display = "block";
    }
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

function displaySnapshot(data) {
    $('#gallery_thumbnails').append('<a href="/cgi-bin/toolkit/image_manager.py?image='+data['name'] +'" rel="thumbnail"><img style="padding:4px; border:2px solid #021a40;" src="/cgi-bin/toolkit/image_manager.py?image='+data['name'].split('.')[0]+'.png" style="width: 64px; height: 64px" /></a>');
    $("#b-pb").remove();
}

