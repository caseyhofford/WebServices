from OBAClient import *
from quickstart import *
import json
from googlemaps import *
import time
import datetime

def processRequest(environ):
    print("entered processRequest")
    method = environ['REQUEST_METHOD']
    parsed = parse(environ)
    if method == "GET" and 'code' in parsed and 'state' in parsed:
        return(makeEventPage(parsed['code'],parsed['state']))
    elif method == "GET" and 'code' in parsed:
        #store code in database associated with IP address
        return(getCal(parsed['code']).encode('utf-8'))
    elif method == "GET":
        return(open('index.html').read().encode('utf-8'))

    elif method == "POST" and 'func' in parsed:
        body = getBody(environ)
        updateCalendar(body)
    elif method == "POST":
        body = getBody(environ)
        summary = getTrip(body)
        return(json.dumps(summary).encode('utf-8'))

def getTrip(parsed):
    origin = parsed['origin']
    destination = parsed['destination']
    arrival = parsed['arrival']
    arrival = arrival + 'Z-0800'
    arrivalstruct = time.strptime(arrival,"%Y-%m-%dT%H %MZ%z")
    print(arrivalstruct)
    arrivalseconds = time.mktime(arrivalstruct)
    print("getTrip:31:  "+str(arrivalseconds))
    route = getRoute(origin['lat'],origin['lon'],destination['lat'],destination['lon'],arrivalseconds)
    stoplat = route[1]['destination']['lat']
    stoplon = route[1]['destination']['lng']
    routename = route[1]['route']
    arrivaltime = route[1]['arrival']
    print("getTrip:35:  "+str(arrivaltime))
    tripId = getTripId(stoplat,stoplon,routename,arrivaltime)
    startlat = route[1]['origin']['lat']
    startlon = route[1]['origin']['lng']
    servicedate = getServiceDate(tripId)
    departurestopid = getStopId(startlat,startlon)
    return({'tripId':tripId,'stopId':departurestopid,'servicedate':servicedate,'arrivalTime':arrivaltime})


def makeEventPage(code,state):
    trip = state.split("-")
    stopId = trip[0]
    serviceDate = trip[1]
    tripId = trip[2]
    arrivalTime = trip[3]
    print("makeEventPage:50:  "+str(arrivalTime))
    departuretime = getArrival(tripId,stopId,serviceDate)
    print("makeEventPage:52:  "+str(departuretime))
    calendar = Calendar(code)
    eventId = calendar.makeEvent(departuretime,arrivalTime,code)
    print("event ID: "+eventId)
    webpage = open("eventtemplate.html")
    template = webpage.read()
    eventpage = template.format(**locals())
    output = open("event.html","w")
    output.write(eventpage)
    output.close()
    return(open("event.html").read().encode("utf-8"))

def updateCalendar(body):
    arrivaltime = getArrival(body['tripId'],body['stopId'],body['serviceDate'])
    updateEvent(body['eventId'],arrivaltime)

def getBody(environ):
    outdict = {}
    try:
        if int(environ['CONTENT_LENGTH']) > 0:
            contentlength = int(environ['CONTENT_LENGTH'])
            outdict = json.loads(environ['wsgi.input'].read(contentlength).decode('utf-8'))
        else:
            outdict = {}
    except ValueError as E:
        print(E)
        outdict['location'] = {}
    return outdict

def parse(environ):
    outdict = {}
    querystring = urllib.parse.parse_qs(environ['QUERY_STRING'])
    if 'func' in querystring:
        outdict['func'] = querystring['func'][0]
    if 'code' in querystring:
        outdict['code'] = querystring['code'][0]
    if 'state' in querystring:
        outdict['state'] = querystring['state'][0]
    return outdict
