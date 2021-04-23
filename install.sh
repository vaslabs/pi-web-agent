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

function prepare_unpack() {
    target=$(mktemp -d)
    cp target/piwebagent2.zip $target/
    echo $target
}

function install_pwa_ca(){
    mkdir $PWA_CA_PATH
    cd $PWA_CA_PATH
	curl -sf https://gobinaries.com/jsha/minica | sh

	minica --domains rpi
    group add pwassl
    sudo chmod 640 $PWA_CA_PATH # group read
    sudo chown root:pwassl -R $PWA_CA_PATH
    usermod -a -G pwassl piwebagent2 # pi web agent can only read
    cd -
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
install_pwa_ca
register_service
start_service
set +e