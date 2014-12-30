$(document).ready(
    function () {
        initialise_services();
});


function initialise_services() {
    processing();
    getJSONResponse('/cgi-bin/toolkit/live_info.py?cmd=services', parseServices);
}

function Service(name, status) {
    self=this;
    self.status = ko.observable(status);
    self.name = ko.observable(name);
    self.killMe = function () {};
    self.submit_service = function () {};
    self.activateMe = function () {};
}

var servicesModel = {services: ko.observableArray()};
function parseServices(services) {
    $.each(services, function (service, status) {
        serviceObj = new Service(service, status);
        servicesModel.services.push(serviceObj);
    });
    ko.applyBindings(servicesModel, document.getElementById("services_area"));
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
