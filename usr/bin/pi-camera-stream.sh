sudo raspivid -o - -t 0 -w 400 -h 300 | cvlc -Idummy -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554/}' :demux=h264
