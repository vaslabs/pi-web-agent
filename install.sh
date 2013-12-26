#!/bin/bash
cd $(dirname $0)
sudo ./setup.sh install || {
    sudo ./setup.sh reinstall
}
cd -
