#!/bin/bash
#Version 0.1
#Description setup tool for the pi-web-agent
#Author: Vasilis Nicolaou
#Copyright (c) CERN 2013
#All rights reserved
VERSION=0.1
APPLICATION_PATH="usr/libexec/pi-web-agent"
SERVICE_PATH="etc/init.d/pi-web-agent"
DEPENDENCIES="tightvncserver apache2 libapache2-mod-dnssd chkconfig"
ANDROID_SERVICE="etc/init.d/pi-android-agent"
VNC_SERVICE="etc/init.d/vncboot"
ETC_PATH="etc/pi-web-agent"
LOGS=/var/log/pi-web-agent
AND_LOGS=/var/log/pi-android-agent
SHARE="usr/share/pi-web-agent"
PI_UPDATE=usr/bin/pi-update
GPIO_BIN=usr/bin/gpio.py
APT_QUERY=usr/bin/apt-query
SUDOERS_D=etc/sudoers.d/pi-web-agent
this_install(){
    echo -n "Installing pi web agent "
    [[ ! -d "/$APPLICATION_PATH" && ! -f "/$SERVICE_PATH" && ! -d "/$ETC_PATH" ]] || {
        print_error "ABORTED"
        echo "The application is already installed. Run \`setup reinstall' if the installation is broken "
        exit 1
    }
    [ -d /usr/libexec ] || mkdir /usr/libexec	
    print_ok
    echo -n "Adding user account for appliance... "
    useradd -r pi-web-agent
    print_ok "DONE"
    sleep 0.5
    /bin/cp -rv "$APPLICATION_PATH" "/$APPLICATION_PATH"
    /bin/cp -av "$SHARE" "/$SHARE"
    /bin/cp -v "$SERVICE_PATH" "/$SERVICE_PATH"
    /bin/cp -v "$ANDROID_SERVICE" "/$ANDROID_SERVICE"
    chmod +x "/$ANDROID_SERVICE"
    chmod +x "/$SERVICE_PATH"
    /bin/cp -rv "$ETC_PATH" "/$ETC_PATH"
    chown -R pi-web-agent "/$APPLICATION_PATH/etc"
    chown -R pi-web-agent:pi-web-agent "/$SHARE"
    echo -n "Starting the pi web agent apache instance daemon "
    [ $? -eq 0 ] || {
        print_error "FAILED"
        echo 
        exit 1
    }
    curr_dir=$(pwd)
    cd /usr/share/pi-web-agent/extras/HTML.py-0.04
    sudo python setup.py install
    cd $curr_dir

    [ -d $LOGS ] || mkdir -p $LOGS
    [ -d $AND_LOGS ] || mkdir -p $AND_LOGS
    cp $VNC_SERVICE /$VNC_SERVICE
    cp $PI_UPDATE /$PI_UPDATE
    cp $GPIO_BIN /$GPIO_BIN
    cp $APT_QUERY /$APT_QUERY
    print_ok
    echo "Installing dependencies"
    apt-get install $DEPENDENCIES
    print_ok
    echo "Post installation actions"    
    chown pi-web-agent:pi-web-agent /usr/libexec/pi-web-agent/.htpasswd
    chown -R pi-web-agent:pi-web-agent /usr/share/pi-web-agent
    chmod 644 /usr/libexec/pi-web-agent/.htpasswd
    print_ok

    echo "Registering pi-web-agent in sudoers"
    cp $SUDOERS_D /$SUDOERS_D
    chown root:root /$SUDOERS_D
    chmod 0440 /$SUDOERS_D

}


this_uninstall() {
    echo "Removing pi web agent"
    this_safe_remove "/$APPLICATION_PATH"

    this_safe_remove "/$ETC_PATH"
    echo -n "Stopping pi web agent apache instance daemon "
    "/$SERVICE_PATH" stop
    this_safe_remove "/$SERVICE_PATH"
    this_safe_remove "/$SHARE"
    print_ok
    echo "Deleting user account of appliance..."
    rm /$SUDOERS_D
    userdel -f pi-web-agent
    print_ok "DONE"
}

this_safe_remove() {
    echo "attempting to remove $1"
    [[ -f "$1" || -d "$1" ]] && {
        echo -n "Removing $1"
        /bin/rm -r "$1"
        [ $? -eq 0 ] || {
            print_error "FAILED"

        }
        print_ok
    }
}

this_reinstall() {
    echo "Reinstalling pi web agent"
    this_uninstall
    this_install
}

print_ok() {
msg="OK"
[ -n "$1" ] && {
   msg=$1
} 
echo -e "[ \e[1;32m $msg \e[0m ]"

}

print_error() {
    echo -e "[ \e[1;31m $1 \e[0m ]"
}

print_warning() {
   echo -e "[ \e[1;33m $1 \e[0m ]"    
}



case $1 in
    install)
        [ $(id -u) -eq 0 ] || {
            echo "You need to be root to run the setup"
            exit 1
        }
        this_install
        exit $?
    ;;
    uninstall)
        [ $(id -u) -eq 0 ] || {
            echo "You need to be root to run the setup"
            exit 1
        }
        this_uninstall
        
        exit $?
    ;;
    reinstall)
        [ $(id -u) -eq 0 ] || {
            echo "You need to be root to run the setup"
            exit 1
        }
        this_reinstall
        
        exit $?
    ;;
    version)
        echo "Version: $VERSION:"
        exit 0
    ;;
    *|?)
        echo "Usage $0 <install|uninstall|reinstall>"
        exit 1
    ;;
esac    

