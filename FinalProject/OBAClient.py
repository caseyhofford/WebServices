#!/bin/python3
import http.client
import json
import urllib
from exceptions import *

#key: 8525e85c-4a2c-4729-8542-f072b45f1c13

def getNearbyStops(lat,lon):#searches for stops near a lat long coordinate
    connection = http.client.HTTPConnection('api.pugetsound.onebusaway.org')
    connection.request('GET','/api/where/stops-for-location.json?key=8525e85c-4a2c-4729-8542-f072b45f1c13&lat='+lat+'&lon='+lon+'&time='+time)
    response = connection.getresponse().read()
    return response

def getStopId(lat,lon):#uses the location search to identify a specific bus stop
    connection = http.client.HTTPConnection('api.pugetsound.onebusaway.org')
    #search for stops by location
    connection.request('GET','/api/where/stops-for-location.json?key=8525e85c-4a2c-4729-8542-f072b45f1c13&lat='+str(lat)+'&lon='+str(lon)+'&radius=1')
    response = json.loads(connection.getresponse().read().decode('utf-8'))
    stopid = response['data']['list'][0]['id']#finds the stop ID
    return stopid

def getTripId(lat,lon,shortName,arrivalepochtime):#finds stop ID, gets the stop schedule, and then finds the route requested and finds the scheduled time for the destination
    connection = http.client.HTTPConnection('api.pugetsound.onebusaway.org')
    #search for stops by location
    connection.request('GET','/api/where/stops-for-location.json?key=8525e85c-4a2c-4729-8542-f072b45f1c13&lat='+str(lat)+'&lon='+str(lon)+'&radius=1')
    response = json.loads(connection.getresponse().read().decode('utf-8'))
    stopid = response['data']['list'][0]['id']
    routes = response['data']['references']['routes']
    routeid = ''
    for route in routes:#finds the routeid based on the routes shortname
        if route['shortName'] == shortName:
            routeid = route['id']
            break
    #search for bus schedule at the stop
    connection = http.client.HTTPConnection('api.pugetsound.onebusaway.org')
    connection.request('GET','/api/where/schedule-for-stop/'+stopid+'.json?key=8525e85c-4a2c-4729-8542-f072b45f1c13')
    response = json.loads(connection.getresponse().read().decode('utf-8'))
    schedules = response['data']['entry']['stopRouteSchedules']
    routeschedule = []
    i = 0
    found = False
    for route in schedules:#find the correct routes schedule for the stop
        if route['routeId'] == routeid:
            found = True
            routeschedule = schedules[i]['stopRouteDirectionSchedules'][0]['scheduleStopTimes']
            break
        i+=1
    if found == False:
        raise OneBusAwayMismatch
    i=0
    bestbus = {}
    for arrival in routeschedule:#find the bus with the closest arrival time
        arrivaltime = arrival['arrivalTime']/1000
        diff = arrivalepochtime-arrivaltime
        if diff > 0:
            bestbus = arrival
        else:
            print("selected bus time: "+ str(arrivaltime))
            break
        i+=1
    tripId = bestbus['tripId']
    #search for trips at stop
    return tripId#returns a string of the tripId

def getServiceDate(tripId):#finds service date by tripId
    connection = http.client.HTTPConnection('api.pugetsound.onebusaway.org')
    connection.request('GET','/api/where/trip-details/'+tripId+'.json?key=8525e85c-4a2c-4729-8542-f072b45f1c13')#returns details about the trip
    response = json.loads(connection.getresponse().read().decode('utf-8'))
    servicedate = response['data']['entry']['serviceDate']
    return(servicedate)#returns an int service date from the tripId in order ro search for an arrival

def getArrival(tripId,stopId,serviceDate):#gets the actual arrival time based on tripId, stopId and serviceDate
    connection = http.client.HTTPConnection('api.pugetsound.onebusaway.org')
    connection.request('GET','/api/where/arrival-and-departure-for-stop/'+stopId+'.json?tripId='+tripId+'&serviceDate='+serviceDate+'&key=8525e85c-4a2c-4729-8542-f072b45f1c13')
    response = json.loads(connection.getresponse().read().decode('utf-8'))
    arrivaltime = response['data']['entry']['predictedArrivalTime']
    if arrivaltime == 0:
        raise PastTripError()
    return arrivaltime#an int with the actual arrival time of the bus at the departure stop

#def getBestRoute(destlat,destlon,lat,lon,arrivaltime):
