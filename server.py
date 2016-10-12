#!/usr/bin/python3
from wsgiref.simple_server import make_server
from wsgiref.util import request_uri
from dispatcher import *
import pprint
import sys

def hello_world_app(environ, start_response):
    try:
        requestsummary = processRequest(environ, storage)#see the processRequest method of dispatcher, returns relevent aspects of eviron as a json object
        #print(requestsummary['content'])
        status = requestsummary['status']  # HTTP Status
        headers = [('Content-type', 'application/json; charset=utf-8')]  # HTTP Headers
        start_response(status, headers)
        return [bytes(str(requestsummary['content']).encode('utf-8'))] #sends json data out as bytes to be decoded by the client
    except NotFoundException as E:
        status = "404 Not Found"  # HTTP Status
        headers = [('Content-type', 'application/json; charset=utf-8')]  # HTTP Headers
        start_response(status, headers)
        print(E)
        return [bytes("404 Not Found".encode('utf-8'))]
    except NegativeQuantity as E:
        status = "400 Bad Request"  # HTTP Status
        headers = [('Content-type', 'application/json; charset=utf-8')]  # HTTP Headers
        start_response(status, headers)
        print(E)
        return [bytes("400 Negative quantity not allowed".encode('utf-8'))]
    except RootDeleteError as E:
        status = "400 Bad Request"  # HTTP Status
        headers = [('Content-type', 'application/json; charset=utf-8')]  # HTTP Headers
        start_response(status, headers)
        print(E)
        return [bytes("403 Forbidden".encode('utf-8'))]
    except ItemOrCategoryMissing as E:
        status = "400 Bad Request"  # HTTP Status
        headers = [('Content-type', 'application/json; charset=utf-8')]  # HTTP Headers
        start_response(status, headers)
        print(E)
        return [bytes("400 Item or category must be specified".encode('utf-8'))]
    except OptionIncorrect as E:
        status = "400 Bad Request"  # HTTP Status
        headers = [('Content-type', 'application/json; charset=utf-8')]  # HTTP Headers
        start_response(status, headers)
        print(E)
        return [bytes("400 Option must be specified".encode('utf-8'))]
    except AuthenticationError as E:
        status = "403 Forbidden"
        headers = [('Content-type', 'application/json; charset=utf-8')]  # HTTP Headers
        start_response(status, headers)
        print(E)
        return [bytes("403 Not Authorized".encode('utf-8'))]

    #capture exceptions to set status codes

#httpd = make_server('', 8000, hello_world_app)
#print("Serving on port 8000...")
#if len(sys.argv) > 1:
#    print(sys.argv)
#    storage = database
#lse:
storage = input('Please choose "database" or "files" for storage')

#Serve until process is killed
#httpd.serve_forever()
