$(function() {
    function Package(data) {
        var self = this;
        var pdata = data[0];
        self.pname = pdata['Package Name'];
        self.installed = pdata['installed'];
        self.version = pdata['Version'];
        self.description = pdata['Description'];
        
        self.submit_package = function submit_package() {
            var url='/cgi-bin/toolkit/installUninstallPackage.py?packageName='+element.name+'&action=';
            
            var param2='install';
            if (self.installed)
            {
               param2='uninstall';
            }
            url+= param2;   
            var info=getResponse(url);

            $('#packages-extension').text("Installation in progress. . .The page will reload in 3 seconds:");
            reloadInXSecs( 3000 );
        };
    
    }
    var viewModel = {
                        packages:ko.observableArray(), 
                        status:ko.observable(true),
                        filter: ko.observable("")
                        
                    };
    
    //filter the items using the filter text
    viewModel.filteredPackages = ko.computed(function() {
        var filter = this.filter().toLowerCase();
        if (!filter) {
            return this.packages();
        } else {
            return ko.utils.arrayFilter(this.packages(), function(item) {
                return item.pname.toLowerCase().indexOf(filter.toLowerCase()) >= 0;
            });
        }
    }, viewModel);                
    
    ko.applyBindings(viewModel, document.getElementById('packages-extension'));
   
    function initPackages(i) {
        if (i > 18)
            return;
        var url = '/cgi-bin/toolkit/package_recommendations.py?index=' + i;
        getJSONResponse(url, addPackage);
        setTimeout(function () {initPackages(i+1);}, 100);
    }
    
    function addPackage(data) {
        viewModel.packages.push(new Package(data));
    }
    
    function getAPTStatus() {
        
    }
    
    initPackages(1);
    
    
    
    
});
