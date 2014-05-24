#!/bin/bash
x-terminal-emulator --command="/usr/bin/execute-pwa.sh" || {
    /usr/bin/execute-pwa.sh
}

