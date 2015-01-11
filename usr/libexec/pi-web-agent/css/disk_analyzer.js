function resetChart() {
    if (typeof(tree) != 'undefined')
    	tree.clearChart();
    initChart($('#path').val()); 
}

function initControls(path) {
    $('#path').val(path == null ? "" : path);
    $('button').click(function(e) { resetChart(); });
}

function checkPath(path) {
    return 0;
}

function initChart(path) {
    // call api to get files and then draw chart
    if (path == null)
        return;
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
    if (items == "Error") {
	endProcessing();
        return;
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

function initDiskAnalyzer(){
    var path = sharedPath;
    sharedPath = "";
    initControls(path)
    initChart(path);
}
$.getScript("https://www.google.com/jsapi", function () {
     google.load("visualization", "1", {callback: 'initDiskAnalyzer', packages:["treemap"]});
     endProcessing()
});
