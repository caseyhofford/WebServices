#API Key: AIzaSyBvD87VOpZZZUOl6mo5vxtTWeUCgN9n2AQ
import http.client
import json


def getRoute(lat,lon,destlat,destlon,arrival_time):
    output = {}
    connection = http.client.HTTPSConnection('maps.googleapis.com')
    strlat = str(lat)
    strlon = str(lon)
    strdestlat = str(destlat)
    strdestlon = str(destlon)
    strarrival = str(arrival_time).split('.')[0]
    URL = '/maps/api/directions/json?origin='+strlat+"%2C"+strlon+'&destination='+strdestlat+"%2C"+strdestlon+'&mode=transit&arrival_time='+strarrival+'&key=AIzaSyBvD87VOpZZZUOl6mo5vxtTWeUCgN9n2AQ'
    connection.request("GET", URL)
    response = json.loads(connection.getresponse().read().decode('utf-8'))
    print(json.dumps(response))
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
        i+=1
    return output
    #returns a JSON object formatted as follows {0: 72, 1: {'route': 'E Line', 'destination': {'lat': 47.6097908, 'lng': -122.337959}, 'arrival': 1476672251}}
    #print(directions['routes'][0]['legs'][0]['steps'][1]['transit_details']['line']['short_name'])
