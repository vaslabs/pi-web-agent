#!/bin/bash

build_dir=$(mktemp -d)
echo "Working directory ${build_dir}"
function copy_system_files() {
    cp -r service/system/lib $build_dir/
    cp -r service/system/etc $build_dir/
}

function copy_backend_main() {
    cp -r service/web/pi-web-agent $build_dir/piwebagent2
}

function copy_ui_assets() {
    mkdir -p $build_dir/usr/share/pi-web-agent/
    cp -r ui/pi-web-agent-app/dist/pi-web-agent-app $build_dir/usr/share/pi-web-agent/assets
}

function zip_app() {
    [ -d target ] && rm -r target
    mkdir -p target/piwebagent2
    mv $build_dir/* target/piwebagent2
    cd target
    zip -r piwebagent2.zip piwebagent2
    cd ..
}

echo "Copying system files"
copy_system_files
echo "Copying piwebagent2 binary"
copy_backend_main
echo "Copying ui assets"
copy_ui_assets
echo "Archiving..."
zip_app