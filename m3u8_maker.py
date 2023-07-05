import os
import re
import datetime
import argparse
import time
from os import walk
from os import path
from natsort import natsorted


def echoTimeStamp(time):
    dt = datetime.datetime.fromtimestamp(time)
    formatted_time = dt.strftime('%H:%M:%S')
    return formatted_time


def create_m3u8_file(file_path, segment_dur, segments,media_sequence):
    with open(file_path, 'w') as f:
        f.write('#EXTM3U\n')
        f.write('#EXT-X-VERSION:3\n')
        f.write('#EXT-X-TARGETDURATION:' + str(segment_dur) + '\n')
        f.write('#EXT-X-MEDIA-SEQUENCE:' + str(media_sequence) + '\n')
        for segment in segments:
            item = segment["url"]
            #print(item)
            year = item[5:9]
            month = item[9:11]
            day = item[11:13]
            f.write(f'#EXTINF:{segment["duration"]},\n')
            time = item[14:24]
            timestamp = int(time)  
            dt = datetime.datetime.fromtimestamp(timestamp)
            print("TS " + echoTimeStamp(timestamp) + " file:" + item)
            formatted_time = dt.strftime('%H:%M:%S')
            #EXT-X-PROGRAM-DATE-TIME:2023-06-30T23:55:08.200+0530
            f.write('#EXT-X-PROGRAM-DATE-TIME:' + str(year) + '-' + str(month) + '-' + str(day) + 'T' +  formatted_time + '.000+0530\n')
            f.write(f'{segment["url"]}\n')
        #f.write('#EXT-X-ENDLIST\n')

def parse_arguments():
    """ Parses the arguments
        directory is required argument
        playlist name defaults to playlist.m3u"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--play-list", default='playlist.m3u', help="playlist name")
    parser.add_argument(
        "-d", "--directory", required=True, help="root directory")
    parser.add_argument(
        "-t", "--timestamp", type=int, required=True, help="start timestamp")
    parser.add_argument(
        "-s", "--segment_dur", type=int, required=True, help="segment duration")
    parser.add_argument(
        '--sort-by-files',
        dest='sort_by_files',
        action='store_true',
        help='sorts list by file name')
    parser.add_argument(
        '--no-sort-by-files',
        dest='sort_by_files',
        action='store_false',
        help='disables file name based sort')
    parser.set_defaults(sort_by_files=False)
    return parser.parse_args()


def get_segments(args,timestamp):

    segments = []

    file_list = os.listdir(args.directory)
    ts_files = [file for file in file_list if file.endswith('.ts')]
    sorted_files = sorted(ts_files)

    select_files = []
    for file_name in sorted_files:
        last_number = re.findall(r'\d+', file_name)[-1]
        if int(last_number) >= timestamp:
            list_size = len(select_files)
            if int(list_size) < 3:
                select_files.append(file_name)

    #for item in select_files:
    #    print(item)

    for item in select_files:
        duration = "{:.4f}".format(float(args.segment_dur)) 
        url = f"{item}"
        segment = {"duration": duration, "url": url}
        segments.append(segment)

    return segments


def create_m3u8_file_in_loop(args):

    timestamp = args.timestamp
    media_sequence = 0

    #echoTimeStamp(timestamp)
    #first time fatching should work fast after that come to normal speed (segment dur)
    print("create_m3u8_file_in_loop " + str(timestamp) + " " +  str(media_sequence) + " " + echoTimeStamp(timestamp))
    segments = get_segments(args,timestamp)
    first_item = segments[0]
    create_m3u8_file(args.play_list,args.segment_dur,segments,media_sequence)

    time.sleep(args.segment_dur -1 )
    timestamp += args.segment_dur

    while(True):
        echoTimeStamp(timestamp)
        segments = get_segments(args,timestamp)
        if first_item != segments[0] :
            media_sequence += 1
            print("create_m3u8_file again media_sequence:" + str(media_sequence) + " TS " + echoTimeStamp(timestamp))
            create_m3u8_file(args.play_list,args.segment_dur,segments,media_sequence)
            timestamp += args.segment_dur
            first_item = segments[0]
        else: 
            print("create_m3u8_file No changes  " + str(timestamp)  + " " +  str(media_sequence) + " " + echoTimeStamp(timestamp))
            timestamp += args.segment_dur

        time.sleep(args.segment_dur)

def main():
    """ Entry point function """

    print("main")

    args = parse_arguments()
    create_m3u8_file_in_loop(args)


if __name__ == '__main__':
    main()