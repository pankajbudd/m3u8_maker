# m3u8_maker
Use to create m3u8 index file base on timestamp provide by user

# m3u8_maker.py commline line 
"-p", "--play-list", default='playlist.m3u', help="playlist name"

"-d", "--directory", required=True, help="root directory"

"-t", "--timestamp", type=int, required=True, help="start timestamp"

"-s", "--segment_dur", type=int, required=True, help="segment duration"

Example

#python3 m3u8_maker.py -p playlist.m3u8 -d ~/Downloads/HLS_indexing/github_code/m3u8_maker/ -t 1688567959 -s 8



# http_server.py commline line 
"-p", "--port", type=int, required=True, help="HTTP server port"

"-c", "--cert-name", default='server.pem', help="certificate filename"

"-s", "--server-name", default='127.0.0.1', help="HTTP server IP"

Exmaple

#python3 http_server.py -p 8002 -s 172.168.1.4 -c cert.pem
