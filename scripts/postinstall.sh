#!/bin/bash

function install_pwa_ca(){
    PWA_CA_PATH='/etc/pwa_ca'
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


echo "Giving permissions to piwebagent to access its static content"
chown piwebagent2 /usr/share/piwebagent2/assets

echo "Setup PWA CA"
install_pwa_ca

echo "Enabling piwebagent2.service"
systemctl enable piwebagent2.service

echo "Starting piwebagent2.service"
systemctl start piwebagent2.service

echo "Giving permissions to the config directory"
chown -R piwebagent2 /etc/piwebagent2/config