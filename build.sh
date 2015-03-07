
working_directory=$(mktemp -d)
CSS_DIR="$working_directory/usr/libexec/pi-web-agent/css"
WDIR="usr/libexec/pi-web-agent/css"
LAST_MAIN="usr/libexec/pi-web-agent/templates/_main_part2.htm"
FIRST_MAIN="usr/libexec/pi-web-agent/templates/_main_part1.htm"
TEMPLATE_DIR="$working_directory/usr/libexec/pi-web-agent/templates"

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
}

minifyCSS() {
    java -jar yuicompressor-2.4.8.jar --type css $CSS_DIR/$1 > pi-web-agent/$WDIR/$1
}

minifyJS() {
    java -jar yuicompressor-2.4.8.jar --type js $CSS_DIR/$1 > pi-web-agent/$WDIR/$1
}

start_compiling() {
    for file in $(ls *.c); do
        filename=$(basename $file '.c')
        gcc $file -o "$filename.pwa"
    done
    rm *.c
}

compilePWA() {
    cd usr/libexec/pi-web-agent/cgi-bin/toolkit
    start_compiling
    cd -
    cd usr/libexec/pi-web-agent/cgi-bin/chrome
    start_compiling
    cd -
    #framework.c must be in source form to allow other developers
    #to include it, no need for compiling it
}

js_to_combine="jquery-1.10.2.min.js bootstrap.min.js bootswatch.js knockout.js system_scripts.js dependency_manager.js general_purpose_scripts.js framework.js"

css_to_combine="blueprint/screen.css bootstrap.css installUninstallSwitch.css"


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
git add .
git commit -m "Version build"
