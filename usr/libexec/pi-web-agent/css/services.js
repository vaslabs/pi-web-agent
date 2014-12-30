$(document).ready(
    function () {
        initialise_services();
});


function initialise_services() {
    processing();
    getJSONResponse('/cgi-bin/toolkit/live_info.py?cmd=services', parseServices);
}

function Service(name, status) {
    var self=this;
    self.status = ko.observable(status);
    self.name = ko.observable(name);
    self.killMe = function () { submit_service(self.name(), false); popSuccessMessage('Kill signal sent to: ' + self.name());};
    
    self.activateMe = function () {submit_service(self.name(), true); popSuccessMessage('Start signal sent to: ' + self.name());};
    self.status.subscribe(function (newValue) {
        if (newValue)
            self.activateMe();
        else
            self.killMe();
    });
}

var servicesModel = {services: ko.observableArray()};
function parseServices(services) {
    $.each(services, function (service, status) {
        serviceObj = new Service(service, status);
        servicesModel.services.push(serviceObj);
    });
    ko.applyBindings(servicesModel, document.getElementById("services_area"));
    $('#services_table').css('display', 'block');
    endProcessing();
}
function submit_service(service_name, status) {
    
     var url='/cgi-bin/toolkit/live_info.py?cmd=edit_service&param1='+service_name;
     var param2='off';
     if (status)
     {
        param2='on';
     }
     url+='&param2=' + param2;   
     var info = getJSONResponse(url, null);
}
