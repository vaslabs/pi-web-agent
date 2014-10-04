function PiWebAgent () {
    self = this;
    
    self.getMainViewElement = function () {
        return $("#extension-main-view");
    };    
}

function View() {
    self = this;
    self.actions = [];
    self.extensions = [
                      ];
    self.extensionsOverflow = [];
    self.extensionLimit = 5;
    fetchViewData();
    
    
    function fetchViewData() {
        data = getJSONResponse('/cgi-bin/chrome/view.pwa', null);
        var extensionsCounter = 0;
        $.each(data[0]["pi-web-agent"].system.actions, function (key, action) {
            if (action.title.split(' ').length >= 3)
                self.extensionsOverflow.push(action);
            else if (extensionsCounter < self.extensionLimit) {
                self.extensions.push(action);
                extensionsCounter++; 
            }
            else
                self.extensionsOverflow.push(action);
                    });
        
        $.each(data[1]["pi-web-agent"].actions, function (key, action) {
            self.actions.push(action);
        });
    };
    
}
$(function() {
    var view = new View();
    ko.applyBindings(view);
});
