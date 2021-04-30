#!/bin/bash

source installation_paths

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

function install_config() {
    mkdir -p /$CONFIG_DIR
    cp $CONFIG_FILE /$CONFIG_FILE
    chown -R piwebagent2 /$CONFIG_DIR
}

function prepare_unpack() {
    target=$(mktemp -d)
    cp target/piwebagent2.zip $target/
    echo $target
}

function install_apt_get_cron_daily() {
    which apt-get && {
        cp $CRON_UPDATE_DAILY /$CRON_UPDATE_DAILY
        chmod +x /$CRON_UPDATE_DAILY
    }
}

function setup_libdir() {
    mkdir -p /$PIWEBAGENT_LIB
    chown -R piwebagent2 /$PIWEBAGENT_LIB
}


work_dir=$(prepare_unpack)
set -e
cd $work_dir
unzip piwebagent2.zip
cd piwebagent2
echo "Installing from $work_dir"
install_binary
install_assets
install_apt_get_cron_daily
create_user
chown piwebagent2 -R /$SHARED_PATH
setup_libdir
install_config
sudoer_user_priviledges
register_service
start_service
set +e