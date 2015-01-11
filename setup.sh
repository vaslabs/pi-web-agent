#!/bin/bash
#Version 0.2
#Description: setup tool for the pi-web-agent
#Author: Vasilis Nicolaou
called_from=$(pwd)
cd $(dirname $0)
VERSION=0.1

source setup_common
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
