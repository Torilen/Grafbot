from http.server import BaseHTTPRequestHandler, HTTPServer
from web.server import MyHandler, setup_interactive
from web.server import SHARED

opt = setup_interactive(SHARED)
MyHandler.protocol_version = 'HTTP/1.0'
httpd = HTTPServer((opt['host'], opt['port']), MyHandler)
print('http://{}:{}/'.format(opt['host'], opt['port']))

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
httpd.server_close()
