
function init() {
    get_controls();
}

function create_controls(data) {
    $( "#slider-vertical" ).slider({
      orientation: "horizontal",
      range: "min",
      min: 0,
      max: 100,
      value: data['volume'],
      stop: function( event, ui ) {
                update_volume(event, ui);
            }
    });
    endProcessing();
    $( "p#amount" ).text( data['volume'] + '%' );
    $('#mute-button').text(data['status'] ? 'Mute' : 'Unmute');
    $('#mute-button').addClass(muteButtonClasses[$('#mute-button').text()]);
}

function update_volume(event, ui) {
    processing();
    url = '/cgi-bin/toolkit/volume_api.py?op=update_vol&mixer=PCM&val=' + ui.value;
	getJSONResponse(url, handle_vol_update)
}

function handle_vol_update(data) {
    $( "p#amount" ).text( data['volume'] + '%' );
    endProcessing();
    return 0;
}

function get_controls() {
    processing();
    url = '/cgi-bin/toolkit/volume_api.py?op=mixers';
    getJSONResponse(url, renderControlsUI);
}

function renderControlsUI(data) {
    $.each(data, function (index, value) {
        var option$ = '<option/>';
        option$ = $(option$).attr('id', value);
        option$ = $(option$).text(value);
        option$ = $(option$).val(value);
        if (index == 0) {
            option$ = $(option$).attr('selected', 'selected');
        }
        $('#control_list').append(option$);
    });
    selectMenu = $("#control_list").selectmenu();
    if (data.length > 0) {
        url = '/cgi-bin/toolkit/volume_api.py?op=get_vol&mixer=' + data[0];
        getJSONResponse(url, create_controls);
    }
    
} 

var muteTextDict = {'Mute':'Unmute', 'Unmute':'Mute'};
var muteButtonClasses = {'Mute':'btn-danger', 'Unmute':'btn-success'}; 

function toggleMute() {
    processing();
    url = '/cgi-bin/toolkit/volume_api.py?op=toggle&mixer=' + selectMenu.val();
    getJSONResponse(url, applyMute);
}

function applyMute(data) {
    
    var currentText = $('#mute-button').text();
    var newText = muteTextDict[currentText];
    var currentClass = muteButtonClasses[currentText];
    var newClass = muteButtonClasses[newText];
    $('#mute-button').removeClass(currentClass);
    $('#mute-button').addClass(newClass);
    $('#mute-button').text(newText);
    $( "#slider-vertical" ).slider( {value:data['volume']} )
    handle_vol_update(data);
    endProcessing();
}

function testSpeakers() {
    url = '/cgi-bin/toolkit/volume_api.py?op=test';
    getJSONResponse(url, null);
}

var selectMenu = null;
$(function() {
    init();
});
