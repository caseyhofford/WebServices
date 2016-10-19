#!/usr/bin/python3
from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server
from dispatcher import *

def simple_app(environ, start_response):

    try:
        response = processRequest(environ)
        status = '200 OK'
        headers = [('Content-type', 'text/html; charset=utf-8')]
        start_response(status, headers)
        return[bytes(response)]
    except PastTripError:
        response = "Go buy a Delorean, you already missed your bus"
        status = '400 Bad Request'
        headers = [('Content-type', 'text/plain; charset=utf-8')]
        start_response(status, headers)
        return[(bytes('Go buy a Delorean, you already missed your bus'.encode('utf-8')))]
    except LocationFormatError:
        response = "And where exactly do you think YOU'RE going? \n please fix your destination request"
        status = '400 Bad Request'
        headers = [('Content-type', 'text/plain; charset=utf-8')]
        start_response(status, headers)
        return[(bytes(response.encode('utf-8')))]
    except CantGetThereFromHere:
        response = "No transit directions found for your locations"
        status = '400 Bad Request'
        headers = [('Content-type', 'text/plain; charset=utf-8')]
        start_response(status, headers)
        return[(bytes(response.encode('utf-8')))]
    except Exception as E:
        #print(E)
        return(bytes(E.encode("utf-8")))

httpd = make_server('', 8000, simple_app)
print("Serving on port 8000...")
httpd.serve_forever()
