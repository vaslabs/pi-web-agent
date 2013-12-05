#!/bin/sh
sudo ./setup.sh reinstall
sudo service pi-web-agent stop
sleep 1s
sudo service pi-web-agent start
sleep 2s
firefox http://127.0.0.1:8004/ &
