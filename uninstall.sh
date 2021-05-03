#!/bin/bash
source installation_paths

function remove_user() {
    userdel piwebagent2
}

function unregister_service() {
    systemctl disable piwebagent2.service
}

function remove_config() {
    rm -r /etc/piwebagent2
}

function stop_service() {
    systemctl stop piwebagent2.service
}

function remove_binary() {
    rm /$BINARY_PATH
}

function remove_assets() {
    rm -r /$SHARED_PATH
}

function unregister_sudoer() {
    rm /$SUDOERS_PATH
}

function remove_certificates() {
    rm -r /etc/pwa_ca || echo "Could not remove piwebagent2 certificates"
    groupdel pwassl || echo "Could not remove pwassl"
}

stop_service || echo "Could not stop service"
unregister_service || echo "Could not unregister service"
unregister_sudoer || echo "Could not remove from sudoers"
remove_user || echo "Could not remove piwebagent2 user"
remove_assets || echo "Could not remove assets"
remove_binary || echo "Could not remove piwebagent2 binary"
remove_config || echo "Could not remove /etc/piwebagent2"
