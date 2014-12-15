var spath="/home/rpi/";
google.load("visualization", "1", {packages:["treemap"]});

function initChart(spath) {
    // call api to get files and then draw chart
    processing();
    alert("Hello, world");
    url = '/cgi-bin/toolkit/disk_analyzer_api.py?op=get_usage&top=' + spath;

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
    alert("Hello, world");
    initChart(spath);
});
