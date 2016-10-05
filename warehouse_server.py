#!/usr/bin/python3
from wsgiref.simple_server import make_server
from wsgiref.util import request_uri
from warehouse_dispatcher import *
import pprint

def hello_world_app(environ, start_response):
    requestsummary = processRequest(environ)#see the processRequest method of dispatcher, returns relevent aspects of eviron as a json object
    status = requestsummary['status']  # HTTP Status
    headers = [('Content-type', 'application/json; charset=utf-8')]  # HTTP Headers
    start_response(status, headers)
    return [bytes(str(requestsummary['content']).encode('utf-8'))] #sends json data out as bytes to be decoded by the client

httpd = make_server('', 8000, hello_world_app)
print("Serving on port 8000...")

# Serve until process is killed
httpd.serve_forever()
