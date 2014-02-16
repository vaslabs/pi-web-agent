#!/bin/bash
cd $(dirname $0)
chmod +x ./setup.sh
sudo ./setup.sh install || {
    sudo ./setup.sh reinstall
}
cd -
