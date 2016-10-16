from OBAClient import *
from quickstart import *
import json

def processRequest(environ):
    print("entered processRequest")
    method = environ['REQUEST_METHOD']
    parsed = parse(environ)

    if method == "GET" and 'code' in parsed:
        return(getCal(parsed['code']).encode('utf-8'))
    elif method == "GET":
        return(open('index.html').read().encode('utf-8'))

    elif method == "POST":
        stops = getNearbyStops(str(parsed['location']['lat']),str(parsed['location']['lon']))
        print(stops)
        return stops
