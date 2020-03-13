#! /usr/bin/env python3

import http.server
import socketserver
import os
import pathlib
import sys
import MarkdocHttpRequestHandler

my_dir = pathlib.Path(__file__).parent.absolute()

if (len(sys.argv) != 2):
    print("wrong number of args")
    sys.exit(1)
md_file = os.path.abspath(sys.argv[1])

os.chdir(my_dir)

PORT = 4000

MarkdocHttpRequestHandler.md_file = md_file

Handler = MarkdocHttpRequestHandler.MarkdocRequestHandler

with socketserver.TCPServer(("",PORT),Handler) as httpd:
    print("serving at port: ", PORT)
    httpd.serve_forever()
    try:
        httpd.serve_forever()
    except:
        print("Closing the server.")
        httpd.server_close()
        raise
