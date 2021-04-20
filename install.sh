#!/bin/bash

SERVICE_PATH=lib/systemd/system/piwebagent2.service
BINARY_PATH=usr/bin/piwebagent2
SHARED_PATH=usr/share/piwebagent2
SUDOERS_PATH=etc/sudoers.d/piwebagent2
function create_user() {
    useradd -r piwebagent2
}

function register_service() {
    cp -r  $SERVICE_PATH /$SERVICE_PATH
    chmod 644 /$SERVICE_PATH
    systemctl enable piwebagent2.service
}

function sudoer_user_priviledges() {
    cp $SUDOERS_PATH /$SUDOERS_PATH
    chmod 400 /$SUDOERS_PATH
}

function start_service() {
    systemctl start piwebagent2.service
}

function install_binary() {
    cp piwebagent2 /$BINARY_PATH
}

function install_assets() {
    cp -r $SHARED_PATH /$SHARED_PATH
}

function prepare_unpack() {
    target=$(mktemp -d)
    cp target/piwebagent2.zip $target/
    echo $target
}

work_dir=$(prepare_unpack)
set -e
cd $work_dir
unzip piwebagent2.zip
cd piwebagent2
echo "Installing from $work_dir"
install_binary
install_assets
create_user
chown piwebagent2 -R /$SHARED_PATH
sudoer_user_priviledges
register_service
start_service
set +e