

function manageInstallationStatusDetection(keys) {
    var remainingIndex = 0;
    for (i=0; i < keys.length; i+= 10) {
        findPackageInstallationStatus(keys.slice(i, i+10));
        remainingIndex = i + 10;
    }
    var keysleft = keys.slice(remainingIndex);
    if (keysleft.length > 0) {
        findPackageInstallationStatus(keysleft);
    }
}

function findPackageInstallationStatus(keys) {
    var url="/cgi-bin/toolkit/pm_api.py?op=check_group&packages="+JSON.stringify(keys);
    getJSONResponse(url, renderInstallationTextBoxes);
}

function go_back() {
    $('#searched_packages_table').remove();
    $('#packages-table-id').css('display', 'block');
    $(".form-group #autocomplete").css('display', 'block');
    $(".form-group #extensive_search").css('display', 'block');
       
    $(".form-group #autocomplete").val("");
    $(".form-group #autocomplete").trigger('keyup');
    $('#go_back_button').remove();
}
