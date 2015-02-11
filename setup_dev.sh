#!/bin/bash
#Version 0.1
#Description: setup tool for the pi-web-agent for use on development mode
#Author: Vasilis Nicolaou
called_from=$(pwd)
cd $(dirname $0)
VERSION=0.1
source setup_common

start_compiling() {
    for file in $(ls *.c); do
        filename=$(basename $file '.c')
        gcc $file -o "$filename.pwa"
    done
    
}

compilePWA() {
    cd usr/libexec/pi-web-agent/cgi-bin/toolkit
    start_compiling
    cd -
    cd usr/libexec/pi-web-agent/cgi-bin/chrome
    start_compiling
    cd -
    cd usr/libexec/pi-web-agent/cgi-bin/
    start_compiling
    cd -
    #framework.c must be in source form to allow other developers
    #to include it, no need for compiling it
}

this_dev_install(){
    echo -n "Installing pi web agent "
    [[ ! -d "/$APPLICATION_PATH" && ! -f "/$SERVICE_PATH" && ! -d "/$ETC_PATH" ]] || {
        print_error "ABORTED"
        echo "The application is already installed. Run \`setup reinstall' if the installation is broken "
        exit 1
    }
    [ -d /usr/libexec ] || mkdir /usr/libexec
    print_ok
    
    
    echo -n "Adding user account for appliance..."
    useradd -r pi-web-agent
    print_ok "DONE"
    sleep 0.5

    [ -f "$htpasswd_PATH" ] || {
         echo -n "Creating password file with default credentials admin:admin "
         htpasswd -cbd "$htpasswd_PATH" 'admin' 'admin' && print_ok "DONE"
    }

    mkdir -p /usr/libexec/pi-web-agent/etc/config/
    
    echo -n "Copying framework file"
    /bin/cp -av usr/libexec/pi-web-agent/etc/config/framework.c /usr/libexec/pi-web-agent/etc/config/framework.c
    echo -n "Installing websocketdBro" 
    chmod +x ./usr/libexec/pi-web-agent/scripts/websocketdBro/raspbian_setup.sh
    ./usr/libexec/pi-web-agent/scripts/websocketdBro/raspbian_setup.sh
    echo -n "Compile pwa files..."
    compilePWA

    /bin/cp -v "$htpasswd_PATH" "/$htpasswd_PATH" 

    /bin/cp -rv "$APPLICATION_PATH"/* "/$APPLICATION_PATH"

    /bin/cp -av "$SHARE" "/$SHARE"
    /bin/cp -v "$SERVICE_PATH" "/$SERVICE_PATH"
    /bin/cp -v "$EXECUTE_BIN" "/$EXECUTE_BIN"
    /bin/cp -v "$PI_APT" "/$PI_APT"
    /bin/cp -v "$UPDATE_APP_BIN" "/$UPDATE_APP_BIN"
    /bin/cp -v "$UPDATE_CHECK_PY" "/$UPDATE_CHECK_PY"
    /bin/cp -v "$SYSTEM_UPDATE_CHECK" "/$SYSTEM_UPDATE_CHECK"
    /bin/cp -v "$STARTUP_PWA" "/$STARTUP_PWA"
    chmod +x "/$EXECUTE_BIN"
    chmod +x "/$SERVICE_PATH"
    chmod +x "/$UPDATE_APP_BIN"
    chmod +x "/$UPDATE_CHECK_PY"
    chmod +x "/$SYSTEM_UPDATE_CHECK"
    chmod +x "/$STARTUP_PWA"
        
    chmod +x $OTHER_BINS
    /bin/cp -v $OTHER_BINS /usr/bin/
    
    touch $CRONJOB_REBOOT
    echo "@reboot root /$STARTUP_PWA" >$CRONJOB_REBOOT

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
    
    echo "Post installation actions"
    chown pi-web-agent:pi-web-agent /usr/libexec/pi-web-agent/.htpasswd
    chown -R pi-web-agent:pi-web-agent /usr/share/pi-web-agent
    chmod 644 /usr/libexec/pi-web-agent/.htpasswd
    print_ok
    echo "Installing wiringPi - examples excluded"
    currDir=$(pwd)
    temp=$(mktemp -d /tmp/wiringPi.XXX)
    cd $temp
    git clone --depth 1 "https://github.com/vaslabs/gordonsWiringPi"
    cd gordonsWiringPi
    chmod +x ./build
    ./build
    echo "DONE"
    cd $currDir
    rm -rf $temp
    cp $CRON_JOBS/* /$CRON_JOBS
    echo "Registering pi-web-agent in sudoers"
    cp $SUDOERS_D /$SUDOERS_D
    chown root:root /$SUDOERS_D
    chmod 0440 /$SUDOERS_D
    chmod 640 "/usr/libexec/pi-web-agent/.htpasswd"
    chown -R pi-web-agent:pi-web-agent /usr/libexec/pi-web-agent
    chmod 770 /usr/libexec/pi-web-agent/cgi-bin/*.py
    chmod 770 /usr/libexec/pi-web-agent/cgi-bin/*.pwa
    chmod 770 /usr/libexec/pi-web-agent/cgi-bin/toolkit/*.py
    chmod 770 /usr/libexec/pi-web-agent/cgi-bin/toolkit/*.pwa
    chmod 770 /usr/libexec/pi-web-agent/html/utilities/*.html
    chmod 770 /usr/libexec/pi-web-agent/html/index.html
    chmod +x /usr/libexec/pi-web-agent/scripts/hostname.sh
    chmod +x /usr/libexec/pi-web-agent/scripts/memory_information
    chmod +x /etc/cron.daily/update-check
    chmod +x /usr/bin/* 
    
    mkdir "/$SHARE/camera-media"
    chown -R pi-web-agent:pi-web-agent "/$SHARE/camera-media"
    
}

this_dev_reinstall() {
    echo "Reinstalling pi web agent"
    echo "Keeping the same password"
    echo -e "\e[0;34m Backing up Camera Snapshots\e[0m"
    cp /$htpasswd_PATH $htpasswd_PATH 
    if [ -d "/$SHARE/camera-media" ]; then
    	mv "/$SHARE/camera-media"  /tmp/.
    else
    	print_error "404 Camera snapshots not found"
    fi
    this_uninstall
    this_dev_install $1
    echo -e "\e[0;34m Restoring Camera Snapshots\e[0m"
    if [ -d "/tmp/camera-media" ]; then
    	cp -af /tmp/camera-media "/$SHARE/"
    	else
    	print_error "Camera snapshots backup not found"
    fi
    echo "Recovering your snapshots"
}

case $1 in
    install)
        [ $(id -u) -eq 0 ] || {
            echo "You need to be reboot to run the setup"
            exit 1
        }
        this_dev_install
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
        this_dev_reinstall
        
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

