google.load("visualization", "1", {packages:["treemap"]});

function getURLParams(url) {
    //returns the GET params in url in a assoc array
    var params = {};
    var paramsStr = url.split("?")[1];

    paramsStr.split("&").map(function(ps) {kv = ps.split("="); params[kv[0]] = kv[1] });
    
    return params;
}

function getPath() {
    var params = getURLParams(document.URL);
    
    return params['path'];
}

function initControls(path) {
    $('#path').val(path);
    var b = $('button').button();

    b.click(function(e) { tree.clearChart(); initChart($('#path').val()) });
}

function initChart(path) {
    // call api to get files and then draw chart
    processing();
    url = '/cgi-bin/toolkit/disk_analyzer_api.py?op=get_usage&top=' + path;

    getJSONResponse(url, drawChart);
}
    
function drawChart(items) {
    items.unshift(["Parent dir", "File", "Size"]);
    
    var data = google.visualization.arrayToDataTable(items);
    tree = new google.visualization.TreeMap(document.getElementById('chart_div'));

    tree.draw(data, {
        minColor: '#f00',
        midColor: '#ddd',
        maxColor: '#0d0',
        headerHeight: 15,
        fontColor: 'black',
        showScale: true
    });

    endProcessing();
}


$(function() {
    var path = getPath();
    initControls(path)
    initChart(path);
});
