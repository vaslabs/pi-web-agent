#!/bin/bash

source installation_paths

function install_pwa_ca(){
    PWA_CA_PATH='/etc/pwa_ca'
    [ -d $PWA_CA_PATH ] || {
        tmp=$(mktemp -d)
        cd $tmp
        git clone https://github.com/jsha/minica.git
        cd minica 
        go build
        mkdir -p $PWA_CA_PATH
        cd $PWA_CA_PATH
        $tmp/minica/minica --domains rpi
        groupadd pwassl
        # group read execute for direcotries
        find $PWA_CA_PATH -type d -print0 | xargs -0 chmod 750
        # group read for files
        find $PWA_CA_PATH -type f -print0 | xargs -0 chmod 640
        sudo chown root:pwassl -R $PWA_CA_PATH
        usermod -a -G pwassl piwebagent2 # pi web agent can only read
        cd -
    }
}

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
install_pwa_ca
chown piwebagent2 -R /$SHARED_PATH
setup_libdir
install_config
sudoer_user_priviledges
register_service
start_service
set +e