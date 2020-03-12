#! /usr/bin/env python3

import http.server
import socketserver

PORT = 4000

Handler = http.server.SimpleHTTPRequestHandler


def prepare():
    paste = ''
    template = ''
    with open('renderme.md', mode='r') as file:
        paste = file.read()
    with open('template.html', mode='r') as file:
        template = file.read()
    print(template)

prepare()

with socketserver.TCPServer(("",PORT),Handler) as httpd:
    print("serving at port: ", PORT)
    httpd.serve_forever()
