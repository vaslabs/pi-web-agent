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
JS_DIR="$working_directory/usr/libexec/pi-web-agent/js"
WDIR="usr/libexec/pi-web-agent"
LAST_MAIN="usr/libexec/pi-web-agent/templates/_main_part2.htm"
FIRST_MAIN="usr/libexec/pi-web-agent/templates/_main_part1.htm"
TEMPLATE_DIR="$working_directory/usr/libexec/pi-web-agent/templates"
sed -i '/VERSION\=/c\VERSION="'$RELEASE'"' $DIR/usr/libexec/pi-web-agent/etc/config/pi_web_agent.py
composeFiles() {
    JS_FILE="temp-$(date +%s).$2"
    echo "" > $working_directory/$WDIR/$2/$JS_FILE
    for file in $1; do
        cat $WDIR/$2/$file >>$working_directory/$WDIR/$2/$JS_FILE
    done
    md5=$(md5sum $working_directory/$WDIR/$2/$JS_FILE | cut -d ' ' -f 1)
    mv $working_directory/$WDIR/$2/$JS_FILE $working_directory/$WDIR/$2/${md5}.$2
    echo ${md5}.$2
}

appendJSToHTML() {
    echo "<html><head><script src='/js/$1'></script>" > $working_directory/$FIRST_MAIN
    
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
    java -jar yuicompressor-2.4.8.jar --type css $CSS_DIR/$1 > $DIR/$WDIR/css/$1
}

minifyJS() {
    java -jar yuicompressor-2.4.8.jar --type js $JS_DIR/$1 > $DIR/$WDIR/js/$1
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

git submodule update --init --recursive
js_to_combine="jquery-2.1.1.min.js materialize.min.js knockout.js system_scripts.js dependency_manager.js appDefinitions.js general_purpose_scripts.js framework.js"

css_to_combine="materialize.min.css jquery-ui.min.css system/css/system.css"


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




