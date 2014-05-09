$(function() {
  var availableTags = [];

  $.ajax({
      url: '/cgi-bin/toolkit/package_recommendations.py?action=getPackageList',
      type: 'get',
      dataType: 'json',
      async: true,
      success: function(data) {
        for (var i = 0 ; i < data.length ; i++) {
          alert(data[i]['label']);
          availableTags.push(data[i]['label']);
        }
      } 
  });


  $( "#autocomplete" ).autocomplete({
  source: availableTags
  });
});
