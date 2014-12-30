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

function resetChart() {
    tree.clearChart();
    initChart($('#path').val()); 
}

function initControls(path) {
    $('#path').val(path);
    $('button').click(function(e) { resetChart(); });
}

function checkPath(path) {
    return 0;
}

function initChart(path) {
    // call api to get files and then draw chart
    processing();
    url = '/cgi-bin/toolkit/disk_analyzer_api.py?op=get_usage&top=' + path;

    getJSONResponse(url, drawChart);
}

function drawChart(items) {

    function readableFileSize(size) {
	var i = Math.floor(Math.log(size) / Math.log(1024));
	return (size / Math.pow(1024, i)).toFixed(2) * 1 + '' + ['B', 'KB', 'MB', 'GB', 'TB'][i];
    }
    
    function showTooltip(row, size, value) {
	return '<div style="background:#fd9; padding:10px; border-style:solid">' +
            '<span style="font-family:Courier"><b>' + data.getValue(row, 0) +
            '</b></span><br>' +
            'Size: ' + readableFileSize(size) + ' </div>';
    }
    
    items.unshift(["Parent dir", "File", "Size"]);
    
    var data = google.visualization.arrayToDataTable(items);
    tree = new google.visualization.TreeMap(document.getElementById('chart_div'));

    tree.draw(data, {
        minColor: '#f00',
        midColor: '#ddd',
        maxColor: '#0d0',
        headerHeight: 15,
        fontColor: 'black',
        showScale: true,
	generateTooltip: showTooltip
    });

    endProcessing();
}


$(document).ready(function(){
    var path = getPath();
    initControls(path)
    initChart(path);
});
