#!/bin/bash

SERVICE_PATH=lib/systemd/system/piwebagent2.service
BINARY_PATH=usr/bin/piwebagent2
SHARED_PATH=usr/share/pi-web-agent
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

stop_service || echo "Could not stop service"
unregister_service || echo "Could not unregister service"
remove_user || echo "Could not remove piwebagent2 user"
remove_assets || echo "Could not remove assets"
remove_binary || echo "Could not remove piwebagent2 binary"