var ext="", apps=[],defaultApps=[], extApps={};
//---default apps- the apps tha can be used on any file
defaultApps.push({"name": "Download", "startFunction":download, "icon": "download.png"});
//--application definition goes here
apps.push({"name": "Mplayer", "startFunction":mplayer, "icon": "mplayer.png", "extensions":[".mp3", ".ogg"]});


//--------start functions go here-------------
//the reason why we need start functions is that later on we can play with iframes
function mplayer(path) {
		window.location='/cgi-bin/toolkit/mplayer.py?uri='+path+'&volume=50';
}
function download(path) {
    window.location='/cgi-bin/toolkit/file_manager.py?download='+path;
}
//---we create an object that holds applications by extension
for( var i=0; i<apps.length;i++) {
	for (var j=0;j<apps[i].extensions.length;j++){
		ext =apps[i].extensions[j]
		if (typeof extApps[ext] ==="undefined"){
				extApps[ext] =[]
		}
		extApps[ext].push(apps[i]);
	}
}

//use the extApps to access the appropriate apps for your file(by roviding its extention)