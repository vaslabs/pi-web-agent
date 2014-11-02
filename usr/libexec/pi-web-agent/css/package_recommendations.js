$(function() {
    function Package(data) {
        var self = this;
        var pdata = data[0];
        self.pname = pdata['Package Name'];
        self.installed = ko.observable(pdata['installed']);
        self.version = pdata['Version'];
        self.description = pdata['Description'];
        
        self.submit_package = function submit_package() {
            var url='/cgi-bin/toolkit/installUninstallPackage.py?packageName='+element.name+'&action=';
            
            var param2='install';
            if (self.installed())
            {
               param2='uninstall';
            }
            url+= param2;   
            var info=getResponse(url);

            $('#packages-extension').text("Installation in progress. . .The page will reload in 3 seconds:");
            reloadInXSecs( 3000 );
        };
    
    }
    
    function updatePackageDefinitions(data, keys, model) {
        $.each(keys, function (pname, index) {
            model.packages()[index].installed(data[pname].installed);
        });
    }
    
    
    function findPackageInstallationStatus(keys, model) {
        var url="/cgi-bin/toolkit/pm_api.py?op=check_group&packages="+JSON.stringify(Object.keys(keys));
        getJSONResponse(url, function (data) {
                                 updatePackageDefinitions(data, keys, model); 
                             }
                       );
    }
    
    
    
    var viewModel = {
        packages:ko.observableArray(),
        backupPackages: null,
        status:ko.observable(true),
        filter: ko.observable(""),
        extensiveSearch: ko.observable(false),
        renderSearchResults: function (data, model) {
            model.backupPackages = model.packages();
            model.packages([]);
            model.extensiveSearch(true);
            $.each(data, function (package_name, package_description) {
                model.packages.push(new Package([{
                    'Package Name': package_name,
                    'Description': package_description,
                    'installed': null,
                    'Version': null
                }]));
            });
            endProcessing();
            var i;
            for (i = 0; i < model.packages().length; i+=10) {
                var keyIndex = {};
                for (var j = i; j < i+10 && j < model.packages().length; j++) {
                    var pname = model.packages()[j].pname;
                    keyIndex[pname] = j;
                }
                findPackageInstallationStatus(keyIndex, model);
            }
            if (i > model.packages().length) {
                var keyIndex = {};
                   
                for (var j = model.packages().length - (i%10); j < model.packages().length; j++) {
                    var pname = model.packages()[j].pname;
                    keyIndex[pname] = j;
                }
                findPackageInstallationStatus(keyIndex, model);
            }
            
        },
        extensive_search: function () {
            var package_name = this.filter();
            if (package_name.length <= 2) {
                popFailMessage("Type more letters or you are really going to slow down your Pi");
                return;
            }
            processing();
            var url="/cgi-bin/toolkit/pm_api.py?op=search&key="+package_name;
            var model = this;
            getJSONResponse(url, function (data) { model.renderSearchResults(data, model);});
        }

        
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
    
    
    initPackages(1);
    
});
