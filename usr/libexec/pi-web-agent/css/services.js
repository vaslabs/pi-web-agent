$(document).ready(
    function () {
        initialise_services();
});

var onoffSwitchHtml = '<div class="onoffswitch">' +
                        '<input type="checkbox" name="service-name" onclick="submit_service(this)" class="onoffswitch-checkbox" id="service-name">'+
                        '<label class="onoffswitch-label" for="service-name">'+
                         '   <div class="onoffswitch-inner"></div>'+
                          '  <div class="onoffswitch-switch"></div>'+
                        '</label>'+
                      '  </div>';

function initialise_services() {
    processing();
    getJSONResponse('/cgi-bin/toolkit/live_info.py?cmd=services', createServicesTable);

}



function createServicesTable(services) {
    $.each(services, function (service, status) {
        var tr$ = '<tr/>';
        var tdName$ = '<td/>';
        var tdSwitch$ = '<td/>';
        tdName$ = $(tdName$).text(service);
        tdSwitch$ = $(tdSwitch$).html(onoffSwitchHtml);
        $($(tdSwitch$).find('input')[0]).attr('name', service);
        $($(tdSwitch$).find('input')[0]).attr('id', service);
        $($(tdSwitch$).find('input')[0]).prop('checked', status);
        $($(tdSwitch$).find('label')[0]).attr('for', service);
        tr$ = $(tr$).append(tdName$);
        tr$ = $(tr$).append(tdSwitch$);
        $('#services_table > tbody').append(tr$);
    });
    endProcessing();
}

function submit_service(element) {
    
     var url='/cgi-bin/toolkit/live_info.py?cmd=edit_service&param1='+element.id;
     var param2='off';
     if (element.checked)
     {
        param2='on';
     }
     url+='&param2=' + param2;   
     var info=getResponse(url, null);
}
