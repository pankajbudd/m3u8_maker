# m3u8_maker
Use to create m3u8 index file base on timestamp provide by user

# m3u8_maker.py commline line 
"-p", "--play-list", default='playlist.m3u', help="playlist name"

"-d", "--directory", required=True, help="root directory"

"-t", "--timestamp", type=int, required=True, help="start timestamp"

"-s", "--segment_dur", type=int, required=True, help="segment duration"

Example

#python3 m3u8_maker.py -p playlist.m3u8 -d m3u8_maker/ -t 1688567959 -s 8



# http_server.py commline line 
"-p", "--port", type=int, required=True, help="HTTP server port"

"-c", "--cert-name", default='server.pem', help="certificate filename"

"-s", "--server-name", default='127.0.0.1', help="HTTP server IP"

Exmaple

#python3 http_server.py -p 8002 -s 172.168.1.4 -c cert.pem


# HLS create using ffmpeg and gstreamer

$ffmpeg -rtsp_transport tcp -i rtsp://... -c:v libx264 -crf 21 -preset veryfast -f hls -strftime 1 -strftime_mkdir 1 -hls_segment_filename file-%Y%m%d-%s.ts out.m3u8

$./gst-launch-1.0 rtspsrc location="rtsp://..." latency=0 name=d is-live=true protocols=4 name=d d. ! application/x-rtp,payload=96 ! rtph264depay ! h264parse config-interval=-1 ! mpegtsmux name=mux ! hlssink playlist-length=100 max-files=10800 \
   playlist-location="stream.m3u8" \
   location="avfragment%06d.ts" target-duration=15  d. ! application/x-rtp,payload=97 ! rtpmp4gdepay ! aacparse ! mux. -e
