from OBAClient import *
from quickstart import *
import json
from googlemaps import *
import time

def processRequest(environ):
    print("entered processRequest")
    method = environ['REQUEST_METHOD']
    parsed = parse(environ)
    print(code)
    if method == "GET" and 'code' in parsed and 'state' in parsed:
        return(getCal(parsed['code']).encode('utf-8'))        
    elif method == "GET" and 'code' in parsed:
        #store code in database associated with IP address
        return(getCal(parsed['code']).encode('utf-8'))
    elif method == "GET":
        return(open('index.html').read().encode('utf-8'))

    elif method == "POST":
        summary = getTrip(parsed)
#        print(str(parsed['origin'])+'\n'+str(parsed['destination'])+'\n'+str(parsed['arrival']))
        return(json.dumps(summary).encode('utf-8'))

def getTrip(parsed):
    origin = parsed['origin']
    destination = parsed['destination']
    arrival = parsed['arrival']
    arrivalstruct = time.strptime(arrival,"%Y-%m-%dT%H %M")
    arrivalseconds = time.mktime(arrivalstruct)
    print("line 28: "+str(arrivalseconds))
    route = getRoute(origin['lat'],origin['lon'],destination['lat'],destination['lon'],arrivalseconds)
    stoplat = route[1]['destination']['lat']
    stoplon = route[1]['destination']['lng']
    routename = route[1]['route']
    arrivaltime = route[1]['arrival']
    print("line 33 dispatcher-arrivaltime: "+str(arrivaltime))
    tripId = getTripId(stoplat,stoplon,routename,arrivaltime)
    startlat = route[1]['origin']['lat']
    startlon = route[1]['origin']['lng']
    servicedate = getServiceDate(tripId)
    departurestopid = getStopId(startlat,startlon)
    print(tripId)
    return({'tripId':tripId,'stopId':departurestopid,'servicedate':servicedate})

code = ''
