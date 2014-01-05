#!/bin/bash
#Version 0.1
#Description setup tool for the pi-web-agent
#Author: Vasilis Nicolaou
#Copyright (c) CERN 2013
#All rights reserved
called_from=$(pwd)
cd $(dirname $0)
VERSION=0.1
APPLICATION_PATH="usr/libexec/pi-web-agent"
SERVICE_PATH="etc/init.d/pi-web-agent"
DEPENDENCIES="tightvncserver apache2 libapache2-mod-dnssd"
ANDROID_SERVICE="etc/init.d/pi-android-agent"
VNC_SERVICE="etc/init.d/vncboot"
ETC_PATH="etc/pi-web-agent"
LOGS=/var/log/pi-web-agent
AND_LOGS=/var/log/pi-android-agent
SHARE="usr/share/pi-web-agent"
PI_UPDATE=usr/bin/pi-update
PI_UPGRADE=usr/bin/pi-upgrade
PI_FIX=usr/bin/pi-fix
APT_QUERY=usr/bin/apt-query
SUDOERS_D=etc/sudoers.d/pi-web-agent
wiringPI=usr/share/wiringPi
GPIO_QUERY=usr/bin/gpio-query
CRON_JOBS=etc/cron.daily
EXECUTE_BIN=usr/bin/execute-pwa.sh
PI_APT=usr/bin/pi-package-management
htpasswd_PATH=usr/libexec/pi-web-agent/.htpasswd
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
    /bin/cp -v "$EXECUTE_BIN" "/$EXECUTE_BIN"
    /bin/cp -v "$PI_APT" "/$PI_APT"
    chmod +x "/$EXECUTE_BIN"
    chmod +x "/$ANDROID_SERVICE"
    chmod +x "/$SERVICE_PATH"
    /bin/cp -rv "$ETC_PATH" "/$ETC_PATH"
    rm -rf "/$ETC_PATH/modules" "/$ETC_PATH/run"
    ln -s "/usr/lib/apache2/modules" "/$ETC_PATH/modules"
    ln -s "/var/run/httpd" "/$ETC_PATH/run"
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
    chmod +x "/$VNC_SERVICE"
    cp $PI_UPDATE /$PI_UPDATE
    cp $PI_UPGRADE /$PI_UPGRADE
    cp $PI_FIX /$PI_FIX
    cp $GPIO_QUERY /$GPIO_QUERY
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
    echo "Installing wiringPi - examples excluded"
    /bin/cp -av $wiringPI /$wiringPI
    cd /$wiringPI
    chmod +x ./build
    ./build
    echo "DONE"
    cd -
    cp $CRON_JOBS/* /$CRON_JOBS
    echo "Registering pi-web-agent in sudoers"
    cp $SUDOERS_D /$SUDOERS_D
    chown root:root /$SUDOERS_D
    chmod 0440 /$SUDOERS_D
    chmod 640 "/usr/libexec/pi-web-agent/.htpasswd"
    chown -R pi-web-agent:pi-web-agent /usr/libexec/pi-web-agent
    chmod 770 /usr/libexec/pi-web-agent/cgi-bin/*.py
    chmod 770 /usr/libexec/pi-web-agent/cgi-bin/toolkit/*.py
    chmod 770 /usr/libexec/pi-web-agent/html/utilities/*.html
    chmod 770 /usr/libexec/pi-web-agent/html/index.html
    chmod +x /usr/libexec/pi-web-agent/scripts/hostname.sh
    chmod +x /usr/libexec/pi-web-agent/scripts/memory_information
    chmod +x /etc/cron.daily/update-check
    chmod +x /usr/bin/*
}


this_uninstall() {
    echo "Removing pi web agent"

    this_safe_remove "/$APPLICATION_PATH"

    this_safe_remove "/$ETC_PATH"
    echo -n "Stopping pi web agent apache instance daemon "
    "/$SERVICE_PATH" stop
    this_safe_remove "/$SERVICE_PATH"
    this_safe_remove "/$SHARE"
    /bin/rm "/$EXECUTE_BIN"
    /bin/rm "/usr/bin/execute.sh"
    /bin/rm "/$PI_APT"
    /etc/init.d/vncboot stop
    rm /etc/init.d/vncboot

    print_ok
    echo "Deleting user account of appliance..."
    rm /$SUDOERS_D
    rm -r /$wiringPI
    rm -r /etc/pi-web-agent
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
    echo "Keeping the same password"
    cp /$htpasswd_PATH $htpasswd_PATH 
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

cd $called_from
