function PiWebAgent () {
    self = this;
    
    self.getMainViewElement = function () {
        return $("#extension-main-view");
    };    
}

function View() {
    var self = this;
    self.actions = [];
    self.categories = {};
    self.catnames = [];
    
    self.navigateTo = function () {
        var img = $("<img/>").attr("src", '/images/' + this.icon).css({'width':'48px', 'height':'48px'});
        $("#extension-title").html('');
        $("#extension-title").append(img);
        $("#extension-title").append(this.title);
        navigate(this.url);
    };
    
    self.insertToCategory = function (cat, action) {
        if (!(cat in self.categories)) {
            self.categories[cat] = [];
            self.catnames.push({'name':cat});
        }
        self.categories[cat].push(action);
    };
    
    
    self.fetchViewData = function () {
        data = getJSONResponse('/cgi-bin/chrome/view.pwa', null);
        var extensionsCounter = 0;
        var allowed2Words = false;
        var allowed = 0;
        $.each(data[0]["pi-web-agent"].system.actions, function (key, action) {
            var category = "Other";
            if ("categories" in action)
            {    $.each(action.categories, function (index, cat) {
                    self.insertToCategory(cat, action);
                });
            }
        });
        
        $.each(data[1]["pi-web-agent"].actions, function (key, action) {
            action.icon = "applications-other-3.png";
            self.insertToCategory("Other", action);
        });
    };
    
    self.fetchViewData();
    
}

$(function() {
    ko.bindingHandlers.foreachprop = {
        transformObject: function (obj) {
            var properties = [];
            for (var key in obj) {
                if (obj.hasOwnProperty(key)) {
                    properties.push({ key: key, value: obj[key] });
                }
            }
            return properties;
        },
        init: function(element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) {
            var value = ko.utils.unwrapObservable(valueAccessor()),
                properties = ko.bindingHandlers.foreachprop.transformObject(value);
            ko.applyBindingsToNode(element, { foreach: properties }, bindingContext);
            return { controlsDescendantBindings: true };
        }
    };
    var view = new View();
    ko.applyBindings(view, document.getElementById("awesome-navbar"));
      $('.button-collapse').sideNav({
          menuWidth: 340, // Default is 240
          edge: 'right', // Choose the horizontal origin
        }
      );
    
    $('#menu-controller').click(function() {
        console.log(status);
        $('.button-collapse').sideNav( 'show' );
    });
    
});


