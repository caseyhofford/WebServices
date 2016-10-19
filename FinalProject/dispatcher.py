from OBAClient import *
from quickstart import *
import json
from googlemaps import *
import time
import datetime
import threading

def processRequest(environ):
    method = environ['REQUEST_METHOD']
    parsed = parse(environ)
    if method == "GET" and 'code' in parsed and 'state' in parsed:
        return(makeEventPage(parsed['code'],parsed['state']))
    elif method == "GET" and 'code' in parsed:
        #store code in database associated with IP address
        return(getCal(parsed['code']).encode('utf-8'))
    elif method == "GET":
        return(open('index.html').read().encode('utf-8'))
    elif method == "PUT":
        body = getBody(environ)
        updateCalendar(body)
    elif method == "POST":
        body = getBody(environ)
        summary = getTrip(body)
        return(json.dumps(summary).encode('utf-8'))

def getTrip(body):
    origin = body['origin']
    destination = body['destination']
    arrival = body['arrival']
    arrival = arrival + 'Z-0600'
    arrivalstruct = time.strptime(arrival,"%Y-%m-%dT%H %MZ%z")
    arrivalseconds = time.mktime(arrivalstruct)
    route = getRoute(origin['lat'],origin['lon'],destination,arrivalseconds)
    stoplat = 0
    stoplon = 0
    routename = ""
    arrivaltime = 0
    walk = 0
    print("getTrip:route details "+str(route))
    for legs in route:
        if type(route[legs]) == dict:
            stoplat = route[legs]['destination']['lat']
            stoplon = route[legs]['destination']['lng']
            routename = route[legs]['route']
            arrivaltime = route[legs]['arrival']
            startlat = route[legs]['origin']['lat']
            startlon = route[legs]['origin']['lng']
            tripId = getTripId(stoplat,stoplon,routename,arrivaltime)
            servicedate = getServiceDate(tripId)
            departurestopid = getStopId(startlat,startlon)
            return({'tripId':tripId,'stopId':departurestopid,'servicedate':servicedate,'arrivalTime':arrivaltime,'walk':walk})
        elif type(route[legs]) == int:
            walk = route[legs]
    raise CantGetThereFromHere("No transit leg found in the google maps trip")

def makeEventPage(code,state):
    trip = state.split("-")
    stopId = trip[0]
    serviceDate = trip[1]
    tripId = trip[2]
    arrivalTime = trip[3]
    walk = trip[4]
    departuretime = getArrival(tripId,stopId,serviceDate)
    calendar = Calendar(code)
    startwalking = departuretime - (int(walk)*1000)
    eventId = calendar.makeEvent(startwalking,arrivalTime,code)
    threading.Timer(3.0, updateCalendar, args=[eventId,tripId,stopId,serviceDate,calendar,departuretime]).start()
    webpage = open("eventtemplate.html")#this functionality is intended to allow the client to receive the trip information for updates to the event
    template = webpage.read()
    eventpage = template.format(**locals())
    output = open("event.html","w")
    output.write(eventpage)
    output.close()
    return(open("event.html").read().encode("utf-8"))

def updateCalendar(eventId,tripId,stopId,serviceDate,calendar,departureTime):
    departureTime = getArrival(tripId,stopId,serviceDate)
    calendar.updateEvent(eventId,departureTime)
    return

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
    if 'func' in querystring:
        outdict['func'] = querystring['func'][0]
    return outdict
