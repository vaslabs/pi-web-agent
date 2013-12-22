$(function() {
$( "#beginning" ).button({
text: false,
icons: {
primary: "ui-icon-seek-start"
}
});
$( "#rewind" ).button({
text: false,
icons: {
primary: "ui-icon-seek-prev"
}
});
$( "#play" ).button({
text: false,
icons: {
primary: "ui-icon-play"
}
})
.click(function() {
var options;
if ( $( this ).text() === "play" ) {
options = {
label: "pause",
icons: {
primary: "ui-icon-pause"
}
};
} else {
options = {
label: "play",
icons: {
primary: "ui-icon-play"
}
};
}
$( this ).button( "option", options );
});
$( "#stop" ).button({
text: false,
icons: {
primary: "ui-icon-stop"
}
})
.click(function() {
$.ajax({
    url: "mplayer_status.py",
    type: "DELETE",
    success: function(result) {
                   if (data.redirect) {
            // data.redirect contains the string URL to redirect to
            location.href=data.redirect;
          }
    }
});
$( "#play" ).button( "option", {
label: "play",
icons: {
primary: "ui-icon-play"
}
});
});
$( "#forward" ).button({
text: false,
icons: {
primary: "ui-icon-seek-next"
}
});
$( "#end" ).button({
text: false,
icons: {
primary: "ui-icon-seek-end"
}
});
$( "#shuffle" ).button();
$( "#repeat" ).buttonset();
});
