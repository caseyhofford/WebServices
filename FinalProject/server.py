#!/usr/bin/python3
from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server
from dispatcher import *

def simple_app(environ, start_response):

    try:
        response = processRequest(environ)
        print("returned from processRequest")
        status = '200 OK'
        headers = [('Content-type', 'text/html; charset=utf-8')]
        start_response(status, headers)
        return[bytes(response)]
    except Exception as E:
        #print(E)
        return(bytes(E.encode("utf-8")))

httpd = make_server('', 8000, simple_app)
print("Serving on port 8000...")
httpd.serve_forever()
