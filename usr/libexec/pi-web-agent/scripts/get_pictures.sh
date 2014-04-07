#!/bin/bash

if [ $# -ne 1 ]; then 
    echo -e "ERROR - Usage:\n\t get_pictures.sh  /path/to/pciture/directory"
    exit 1
fi

if [ ! -d $1 ]; then
    echo -e "ERROR - Not a directory: $1"
    exit 1
fi

find $1 -iname "*.jpg";

exit 0;
