#!/bin/bash
source installation_paths

function remove_user() {
    userdel piwebagent2
}

function unregister_service() {
    chmod 755 /$SERVICE_PATH
    systemctl disable piwebagent2.service
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

stop_service || echo "Could not stop service"
unregister_service || echo "Could not unregister service"
unregister_sudoer || echo "Could not remove from sudoers"
remove_user || echo "Could not remove piwebagent2 user"
remove_assets || echo "Could not remove assets"
remove_binary || echo "Could not remove piwebagent2 binary"