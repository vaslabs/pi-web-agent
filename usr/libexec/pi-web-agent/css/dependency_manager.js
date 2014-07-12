function getDependenciesFor(pkg) {
    var dmurl='//cgi-bin/toolkit/package_manager.py?p=' + pkg;

    var jqxhr = $.getJSON( dmurl, function() {
        
    })
    .done( function (data) {
        buildPackageManagerView(data);
    });
}


function buildPackageManagerView(data) {
    $("#dialog").dialog({title: 'Dependency Manager'});
    $("#dialog_content").text(data);

}
