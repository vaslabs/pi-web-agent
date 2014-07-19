

function buildPackageManagerView(data) {
    $("#dialog").dialog({title: 'Dependency Manager', width: "75%"});
    $("#dialog_content").html('');
    $("#dialog_content").html("<table id='packages-table-id'></table>");
    buildHtmlTableFromObject(data, 'packages-table-id', ['Version', 'Description', 'Status']);
    endProcessing();
}


function getDependenciesFor(pkg) {
    var dmurl='/cgi-bin/toolkit/package_manager.py?p=' + pkg;
    processing();
    
    getJSONResponse(dmurl, buildPackageManagerView);    
}

