from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import paths, requests
from .StopRunWebserver import StopRunWebserver
import os.path as op
import datetime
from .util import makedirs
import logging

class Sx5Webserver(HTTPServer):
    DEFAULT_SERVER_PORT = 2222
    DEFAULT_SERVER_IP = ""
    keep_running = 1

    def __init__(self, *args, **kw):
        HTTPServer(("192.168.119.140", self.DEFAULT_SERVER_PORT), StopRunWebserver)


    def serve_forever(self):
        while not self.keep_running:
            self.handle_request()


    def force_stop(self):
        self.server_close()
        self.keep_running = 0
        self.create_dummy_request()


    def create_dummy_request(self):
        server = requests.post("http://192.168.119.140:"+self.DEFAULT_SERVER_PORT)
        print("Fake request created from our class!")

    