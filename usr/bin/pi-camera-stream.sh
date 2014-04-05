sudo raspivid -o - -t 9999999 -w 400 -h 300 | cvlc -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554/}' :demux=h264
