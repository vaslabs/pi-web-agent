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

            $('#packages-table').text("Installation in progress. . .The page will reload in 3 seconds:");
            reloadInXSecs( 3000 );
        };
    
    }
    var viewModel = {
                        packages:ko.observableArray(), 
                        status:ko.observable(true)
                    };
    ko.applyBindings(viewModel, document.getElementById('packages-table-id'));
   
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
    
    //filter the items using the filter text
    viewModel.filteredItems = ko.computed(function() {
        var filter = this.filter().toLowerCase();
        if (!filter) {
            return this.items();
        } else {
            return ko.utils.arrayFilter(this.items(), function(item) {
                return ko.utils.stringStartsWith(item.pname().toLowerCase(), filter);
            });
        }
    }, viewModel);
    
    
});
