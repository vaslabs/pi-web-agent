RELEASE=$1
if [ -z "$RELEASE" ]; then
	echo "Please enter release name:"
	read RELEASE
fi
working_directory=$(mktemp -d)
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd );
echo "setting up yui compressor ..."
[ ! -f ~/yuicompressor-2.4.8.jar ] && cd ~ && { curl -O -L https://github.com/yui/yuicompressor/releases/download/v2.4.8/yuicompressor-2.4.8.jar ; cd -; }
CSS_DIR="$working_directory/usr/libexec/pi-web-agent/css"
WDIR="usr/libexec/pi-web-agent/css"
LAST_MAIN="usr/libexec/pi-web-agent/templates/_main_part2.htm"
FIRST_MAIN="usr/libexec/pi-web-agent/templates/_main_part1.htm"
TEMPLATE_DIR="$working_directory/usr/libexec/pi-web-agent/templates"
sed -i '/VERSION\=/c\VERSION="'$RELEASE'"' $DIR/usr/libexec/pi-web-agent/etc/config/pi_web_agent.py
composeFiles() {
    JS_FILE="$2.$2"
    echo "" > $CSS_DIR/$JS_FILE
    for part in $1; do
        cat $WDIR/$part >>$CSS_DIR/$JS_FILE
    done
    md5=$(md5sum $CSS_DIR/$JS_FILE | cut -d ' ' -f 1)
    mv $CSS_DIR/$JS_FILE $CSS_DIR/${md5}.$2
    echo ${md5}.$2
}

appendJSToHTML() {
    echo "<html><head><script src='/css/$1'></script>" > $working_directory/$FIRST_MAIN
    
}

appendCSSToHTML() {
    mv $FIRST_MAIN $FIRST_MAIN.prebuild; 
    grep -v -x -f $FIRST_MAIN.buildDiff $FIRST_MAIN.prebuild >  $FIRST_MAIN;
    rm $FIRST_MAIN.prebuild;    
    echo "<link rel='stylesheet' href=/css/$1 type='text/css'>" >>$working_directory/$FIRST_MAIN
    cat $FIRST_MAIN >> $working_directory/$FIRST_MAIN
    sudo cp $working_directory/$FIRST_MAIN $FIRST_MAIN
    sed -i '/Version/c\<div align="center" id="footer">Version: $RELEASE, Copyright © pi-web-agent community 2014' $FIRST_MAIN
}

minifyCSS() {
    java -jar yuicompressor-2.4.8.jar --type css $CSS_DIR/$1 > $DIR/$WDIR/$1
}

minifyJS() {
    java -jar yuicompressor-2.4.8.jar --type js $CSS_DIR/$1 > $DIR/$WDIR/$1
}

start_compiling() {
    for file in $(ls *.c); do
        filename=$(basename $file '.c')
        gcc $file -o "$filename.pwa"
    done
    rm *.c
}

compilePWA() {
	 #compiled files include the framework.c file 
	 #from /usr/libexec/pi-web-agent/etc/config/framework.c
	 #so we should set it up first:
    rm $DIR/.gitignore
    sudo cp --parents $DIR/usr/libexec/pi-web-agent/etc/config/framework.c /
    cd $DIR/usr/libexec/pi-web-agent/cgi-bin/toolkit
    start_compiling
    cd -
    cd $DIR/usr/libexec/pi-web-agent/cgi-bin/chrome
    start_compiling
    cd -
    cd $DIR/usr/libexec/pi-web-agent/cgi-bin
    start_compiling
    cd -
    #framework.c must be in source form to allow other developers
    #to include it, no need for compiling it
}
if [ -z "$RELEASE" ]; then
	echo -e "This build will \e[0;34m not \e[0m be used for a release"
else
	echo -e "This build will be used for Release:\e[0m $RELEASE \e[0m"
	echo -e "Creating Branch \e[0;34m $RELEASE\e[0m"
	git checkout -b "$RELEASE"
	echo "Pushing new branch to origin"
	git push origin "$RELEASE"
	echo "Now your branches are:"
	git branch
fi;
js_to_combine="jquery-1.10.2.min.js bootstrap.min.js bootswatch.js knockout.js system_scripts.js dependency_manager.js appDefinitions.js general_purpose_scripts.js framework.js"

css_to_combine="blueprint/screen.css bootstrap.css installUninstallSwitch.css system/css/system.css"


mkdir -p $CSS_DIR

COMBINED_JS=$(composeFiles "$js_to_combine" "js")
COMBINED_CSS=$(composeFiles "$css_to_combine" "css")

echo $COMBINED_JS
echo $COMBINED_CSS

mkdir -p $TEMPLATE_DIR

template=$(appendJSToHTML $COMBINED_JS)
echo $template
template=$(appendCSSToHTML $COMBINED_CSS)
echo $template

cd ~ #place yuicompressor-2.4.8.jar to home
minifyCSS $COMBINED_CSS
minifyJS $COMBINED_JS
cd -

compilePWA

#commit current state
if [ ! -z "$RELEASE" ]; then
	git add .
	git commit -m "Version build for release $RELEASE"
	git push origin "$RELEASE"
fi;



