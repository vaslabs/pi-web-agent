function PiWebAgent () {
    self = this;
    
    self.getMainViewElement = function () {
        return $("#extension-main-view");
    };    
}

function View() {
    self = this;
    self.actions = null;
    self.extensions = null;
    fetchViewData();
    
    
    function fetchViewData() {
        data = getJSONResponse('/cgi-bin/chrome/view.pwa');
        self.extensions = data[0]["pi-web-agent"].system.actions;
        self.actions = data[1]["pi-web-agent"].actions;
    }
    
}
ko.applyBindings(new View());
