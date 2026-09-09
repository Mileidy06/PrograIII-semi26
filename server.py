from http.server import HTTPServer, simpleHTTPRequestHandler
from urllib import parse
from urllib.parse import urlparse, parse_qs

import json

port = 3000

class miServidor(simpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = "/index.html"
            return simpleHTTPRequestHandler.do_GET(self)

print (f"Servidor corriendo  en el puerto{port}")
server = HTTPServer(("localhost",port),miServidor)
server.serve_forever()

