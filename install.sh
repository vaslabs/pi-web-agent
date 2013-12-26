#!/bin/bash
sudo ./setup install || {
    sudo ./setup reinstall
}
