
var submit_package = function() {
    var url='/cgi-bin/toolkit/installUninstallPackage.py?packageName=' + $(this).attr('id') + '&action=';
    
    var param2='install';
    if (!$(this).prop('checked'))
    {
       param2='uninstall';
    }
    url+= param2;
    var info=getResponse(url);

    $(this).prop('checked', $(this).prop('checked'));
        
};

function buildPackageManagerView(data) {
    $("#dialog").dialog({title: 'Dependency Manager', width: "75%"});
    $("#dialog_content").html('');
    $("#dialog_content").html("<table id='packages-table-id'></table>");
    
    $.each(data, function (pname, pkg) {
        data[pname]['Status'] = generateCheckBox(pkg);
    });
    
    buildHtmlTableFromObject(data, 'packages-table-id', ['Version', 'Description', 'Status']);
    endProcessing();
}


function getDependenciesFor(pkg) {
    var dmurl='/cgi-bin/toolkit/package_manager.py?p=' + pkg;
    processing();
    
    getJSONResponse(dmurl, buildPackageManagerView); 
}

function generateCheckBox(data) {
    var divSwitch = $('<div/>').addClass('on_off_switch');
    var input = $('<input/>').attr('type', 'checkbox')
                            .attr('name', data['Package Name'])
                            .attr('id', data['Package Name'])
                            .prop('checked', !data.installed)
                            .click(submit_package)
                            .addClass('on_off_switch-checkbox');
    var label = $('<label/>').addClass("on_off_switch-label")
                            .attr('for', data['Package Name'])
                            .html('<div class="on_off_switch-inner"></div><div class="on_off_switch-switch"></div>');
    
    divSwitch.append(input).append(label);
    return divSwitch;
}




