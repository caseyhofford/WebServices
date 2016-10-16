#!/bin/python3
import http.client
import json
import urllib

#key: 8525e85c-4a2c-4729-8542-f072b45f1c13

def parse(environ):
    outdict = {}
    try:
        if int(environ['CONTENT_LENGTH']) > 0:
            print('parsing content')
            contentlength = int(environ['CONTENT_LENGTH'])
            body = json.loads(environ['wsgi.input'].read(contentlength).decode('utf-8'))
            print(body)
            outdict['location'] = body['location']
        else:
            outdict['location'] = {}
    except Exception:
        outdict['location'] = {}
    querystring = urllib.parse.parse_qs(environ['QUERY_STRING'])
    if 'func' in querystring:
        outdict['func'] = querystring['func'][0]
    if 'code' in querystring:
        outdict['code'] = querystring['code'][0]
    return outdict


def getNearbyStops(lat,lon):
    print('getting nearby stops')
    connection = http.client.HTTPConnection('api.pugetsound.onebusaway.org')
    connection.request('GET','/api/where/stops-for-location.json?key=8525e85c-4a2c-4729-8542-f072b45f1c13&lat='+lat+'&lon='+lon)
    response = connection.getresponse().read()
    return response

def getBestRoute(destlat,destlon,lat,lon,arrivaltime):
