#!/bin/bash
cd $(dirname $0)
sudo ./setup install || {
    sudo ./setup reinstall
}
cd -
