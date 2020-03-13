#! /usr/bin/env python3

import http.server
import socketserver
import os
import pathlib
import sys
import MarkdocHttpRequestHandler
import wx

my_dir = pathlib.Path(__file__).parent.absolute()

def get_path(wildcard):
    app = wx.App(None)
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    dialog = wx.FileDialog(None, 'Open', wildcard=wildcard, style=style)
    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
    else:
        path = None
    dialog.Destroy()
    return path

md_file = ''

if (len(sys.argv) != 2):
    md_file = os.path.abspath(get_path('*.mdoc'))
else:
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
