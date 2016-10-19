#API Key: AIzaSyBvD87VOpZZZUOl6mo5vxtTWeUCgN9n2AQ
import http.client
import json
import time
from exceptions import *
import urllib.parse

def getRoute(lat,lon,destination,arrival_time):#finds a transit route between two locations (one as any string and one as lat lon) and returns each leg, walking as an int and transit as a dict
    output = {}
    connection = http.client.HTTPSConnection('maps.googleapis.com')
    strlat = str(lat)#must be string from URL
    strlon = str(lon)
    strarrival = str(arrival_time).split('.')[0]
    URLdict = {}
    URLdict['origin'] = strlat+","+strlon
    URLdict['destination'] = destination
    URLdict['mode'] = 'transit'
    URLdict['arrival_time'] = strarrival
    URLdict['key'] = 'AIzaSyBvD87VOpZZZUOl6mo5vxtTWeUCgN9n2AQ'
    qs = urllib.parse.urlencode(URLdict)
    URL = '/maps/api/directions/json?'+qs
    connection.request("GET", URL)
    resp = connection.getresponse().read().decode('utf-8')
    response = json.loads(resp)
    if response['status'] == "ZERO_RESULTS":#google maps response when there is no route
        raise CantGetThereFromHere("No transit route found for this request")
    if response['status'] == "NOT_FOUND":#googles response when a location is incorrect
        raise LocationFormatError("Destination was not found")
    print("Google Maps Status: "+response['status'])
    leavetime = response['routes'][0]['legs'][0]['departure_time']['value']
    if leavetime < time.time():
        raise PastTripError()
    steps = response['routes'][0]['legs'][0]['steps']
    i = 0
    for index in steps:
        if steps[i]['travel_mode'] == 'WALKING':
            output[i] = steps[i]['duration']['value']
        elif steps[i]['travel_mode'] == 'TRANSIT':
            output[i] = {}
            output[i]['route'] = steps[i]['transit_details']['line']['short_name']
            output[i]['arrival'] = steps[i]['transit_details']['arrival_time']['value']
            output[i]['origin'] = steps[i]['start_location']
            output[i]['destination'] = steps[i]['end_location']
            print("GMaps expected transit Departure: "+str(steps[i]['transit_details']['departure_time']['value']))
        i+=1
    return output
    #returns a JSON object formatted as follows {0: 72, 1: {'route': 'E Line', 'destination': {'lat': 47.6097908, 'lng': -122.337959}, 'arrival': 1476672251}}
