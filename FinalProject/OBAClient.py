#!/bin/python3
import http.client
import json
import urllib

#key: 8525e85c-4a2c-4729-8542-f072b45f1c13

def getNearbyStops(lat,lon):
    print('getting nearby stops')
    connection = http.client.HTTPConnection('api.pugetsound.onebusaway.org')
    connection.request('GET','/api/where/stops-for-location.json?key=8525e85c-4a2c-4729-8542-f072b45f1c13&lat='+lat+'&lon='+lon+'&time='+time)
    response = connection.getresponse().read()
    return response

def getStopId(lat,lon):
    connection = http.client.HTTPConnection('api.pugetsound.onebusaway.org')
    #search for stops by location
    connection.request('GET','/api/where/stops-for-location.json?key=8525e85c-4a2c-4729-8542-f072b45f1c13&lat='+str(lat)+'&lon='+str(lon)+'&radius=1')
    response = json.loads(connection.getresponse().read().decode('utf-8'))
    stopid = response['data']['list'][0]['id']
    return stopid

def getTripId(lat,lon,shortName,arrivalepochtime):
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
    for route in schedules:#find the correct routes schedule for the stop
        if route['routeId'] == routeid:
            routeschedule = schedules[i]['stopRouteDirectionSchedules'][0]['scheduleStopTimes']
            break
        i+=1
    i=0
    bestbus = {}
    for arrival in routeschedule:#find the bus with the closest arrival time
        arrivaltime = arrival['arrivalTime']/1000
        diff = arrivalepochtime-arrivaltime
        print("line 75: "+str(diff))
        if diff > 0:
            bestbus = arrival
        else:
            break
        i+=1
    tripId = bestbus['tripId']
    #search for trips at stop
    return tripId

def getServiceDate(tripId):
    connection = http.client.HTTPConnection('api.pugetsound.onebusaway.org')
    connection.request('GET','/api/where/trip-details/'+tripId+'.json?key=8525e85c-4a2c-4729-8542-f072b45f1c13')
    response = json.loads(connection.getresponse().read().decode('utf-8'))
    servicedate = response['data']['entry']['serviceDate']
    return(servicedate)

def getArrival(tripId,stopId,serviceDate):
    connection = http.client.HTTPConnection('api.pugetsound.onebusaway.org')
    connection.request('GET','/api/where/arrival-and-departure-for-stop/'+stopId+'.json?tripId='+tripId+'&serviceDate='+serviceDate+'&key=8525e85c-4a2c-4729-8542-f072b45f1c13')
    response = json.loads(connection.getresponse().read().decode('utf-8'))
    return response['data']['entry']['predictedArrivalTime']

#def getBestRoute(destlat,destlon,lat,lon,arrivaltime):
