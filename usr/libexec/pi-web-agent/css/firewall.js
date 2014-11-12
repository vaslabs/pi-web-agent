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

function initialise_iptables() {
    processing();
    iptablesURL = '/cgi-bin/toolkit/pi_iptables_api.py';
    getJSONResponse(iptablesURL, renderUI);
}

function flush(chain) {
    var url = '/cgi-bin/toolkit/pi_iptables_api.py?flush=' + chain;
    processing();
    getJSONResponse(url, reload_firewall);
}


function renderUI(data) {
    $.each(data, function (chain_name, chain_rules) {
        var header = '<h4 style="float: left;"><a href="#" onclick="firewall_dialog(\'' + chain_name + '\')">'
                     + chain_name + '</a>'+' (Default Protocol: ' + chain_rules['default'] + ')</h4>' + 
                     '<button class="btn btn-danger" style="float:right;" onclick="flush(\'' + chain_name + '\');">Clear rules</button>';
        var table = '<table border="1" cellpadding="4" class="rule_table" id="' + chain_name + '"></table>'
        $("#firewall_area").append(header);
        $("#firewall_area").append(table);
        addColumnHeadersToTable(chain_name, 
                    ['protocol', 'target', 'otherinfo', 'destination', 'source', 'option']);
        var rules = chain_rules['rules'];
        
        if (rules.length == 0) {
            insertRow(chain_name, '--', '--', '--', '--', '--', '--');
        }
        else {
            $.each(rules, function (index, rule) {
                insertRow(chain_name, rule['protocol'], rule['target'], 
                                      rule['otherinfo'], rule['destination'],
                                      rule['source'], rule['option']);
            });
        }
        
    });
    endProcessing();

}

function insertRow(tableID, protocol, target, otherinfo, destination, source, option) {
    var rowContent = '<td>' + protocol + '</td>' +
                    '<td>' + target + '</td>' +
                    '<td>' + otherinfo + '</td>' +
                    '<td>' + destination + '</td>' +
                    '<td>' + source + '</td>' +
                    '<td>' + option + '</td>';
    var row = '<tr>' + rowContent + '</tr>';
    
    $('#' + tableID + ' > tbody').append(row);
}

function firewall_dialog(chain) {
    $('#ip_overlay').remove();
    showDialog('Chain: ' + chain, overlay);
    $('#ip_overlay').data("chain", chain);
    
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
        var chain = $('#ip_overlay').data('chain');
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
    processing();
    closeDialog();
    var url='/cgi-bin/toolkit/add_iptable_rules.py?chain='+chain+'&action='+action+'&protocol='+protocol+'&ipaddress='+ip_address;
    $.ajax({
        type: "GET",
        url: url,
        async: true,
        success : function(data) {
            endProcessing();
            reload_firewall();
        }
    });
    
    //return value;
}

function reload_firewall() {
    $('.ui-dialog').remove();
    processing();
    navigate('/cgi-bin/toolkit/pi_iptables.py?type=js');
}


var overlay = null;

$( function () {
    initialise_iptables();
    enableProtocolRule();
    enableIPRule();
    overlay = $('#ip_overlay_holder').html();
    $('#ip_overlay_holder').remove();   
});
