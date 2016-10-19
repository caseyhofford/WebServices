#import os
from apiclient import discovery
from oauth2client import client
#from oauth2client import tools
#from oauth2client.file import Storage
import datetime
import httplib2
import time

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'BusNotifier'

#def get_authurl():
#    auth_uri = flow.step1_get_authorize_url()
#    return({'flow':flow,'uri':auth_uri})

class Calendar():


    def __init__(self,code):
        self.flow = client.flow_from_clientsecrets('client_secret.json',scope='https://www.googleapis.com/auth/calendar',redirect_uri='http://127.0.0.2:8000')
        authorization = code
        self.credentials = self.flow.step2_exchange(authorization)
        http = self.credentials.authorize(httplib2.Http())
        self.service = discovery.build('calendar', 'v3', http=http)

    def makeEvent(self,departuretime,arrivaltime,code):#sends an event to Gcal from the times and an oauth code
        rfcdeparture = time.strftime('%Y-%m-%dT%H:%M:%S',time.gmtime(int(departuretime)/1000))
        rfcarrival = time.strftime('%Y-%m-%dT%H:%M:%S',time.gmtime(int(arrivaltime)))
        print("makeEvent:60:departuretime: "+str(departuretime))
        body = {
          'summary': 'Bus Ride',
          'start': {
            'dateTime': rfcdeparture,
            'timeZone': 'Etc/GMT',
          },
          'end': {
            'dateTime': rfcarrival,
            'timeZone': 'Etc/GMT',
          },
          'reminders': {
            'useDefault': False,
            'overrides': [
              {'method': 'email', 'minutes': 10},
              {'method': 'popup', 'minutes': 10},
              {'method': 'popup', 'minutes': 5},
            ],
          },
        }
        event = self.service.events().insert(calendarId='primary',sendNotifications=True, fields="id,start/dateTime", body=body ).execute()
        return(event['id'])

    def updateEvent(self,eventId,startTime):
        event = self.service.events().get(calendarId='primary', eventId=eventId).execute()
        event['start']['datetime'] = startTime
        updated_event = self.service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
        return
