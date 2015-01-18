#!/bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd );
#SCRIPTDIR="$(dirname "$DIR")"
pidof websocketd||"$DIR"/websocketdBro/bro -m consumer -c "$4" -k "$5" -e mplayer </dev/null >/dev/null 2>&1 &
sh -c '[ -p /tmp/mplayer-control ]|| mkfifo /tmp/mplayer-control;
sudo amixer cset numid=3 "$0"; 
sudo mplayer -slave -input file=/tmp/mplayer-control -ao alsa:device=hw -af equalizer=0:0:0:0:0:0:0:0:0:0 -volume "$1" "$2" | grep -Po "KVolume.*?$|Title.*$|Album.*$|Year.*$|Track.*?$|Name.*$|Website.*?$|Genre.*?$" |while IFS= read -r line; do echo $line |"$3"/websocketdBro/bro -m publisher -e mplayer; done' $1 $2 $3 $DIR >test &
echo '"$1"\n0:0:0:0:0:0:0:0:0:0' > /tmp/mplayer_status
