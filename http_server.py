# taken from http://www.piware.de/2011/01/creating-an-https-server-in-python/
# generate server.xml with the following command:
#    openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes
# run as follows:
#    python simple-https-server.py
# then in your browser, visit:
#    https://localhost:8000

from http.server import SimpleHTTPRequestHandler, HTTPServer
import ssl
import os
import argparse
import subprocess

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def parse_arguments():
    """ Parses the arguments
        directory is required argument
        playlist name defaults to playlist.m3u"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--port", type=int, required=True, help="HTTP server port")
    parser.add_argument(
        "-c", "--cert-name", default='server.pem', help="certificate filename")
    parser.add_argument(
        "-s", "--server-name", default='127.0.0.1', help="HTTP server IP")

    return parser.parse_args()

def process(args):
    # Create an HTTP server with the CORSRequestHandler
    server_address = (args.server_name, args.port)

    httpd = HTTPServer(server_address, CORSRequestHandler)

    print("certificate " + args.cert_name)

	# Enable HTTPS by providing the path to the SSL/TLS certificate and key files
    httpd.socket = ssl.wrap_socket (httpd.socket, certfile=args.cert_name, server_side=True)

    print("HTTPS server running at " + str(args.port))
    print("https://" + str(args.server_name) + ":" + str(args.port) +  str("/"))

	# Start the server
    httpd.serve_forever()

def main():
    """ Entry point function """

    args = parse_arguments()
    process(args)

if __name__ == '__main__':
    main()
