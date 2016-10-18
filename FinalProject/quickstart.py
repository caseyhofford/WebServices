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
        print(code)
        authorization = code
        self.credentials = self.flow.step2_exchange(authorization)

    def getCal(self,code):
        """Shows basic usage of the Google Calendar API.

        Creates a Google Calendar API service object and outputs a list of the next
        10 events on the user's calendar.
        """
        output = ''
        #credentials = getCredentials(code)
        http = self.credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        eventsResult = service.events().list(
            calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])

        if not events:
            return('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            output+=(start +" " +event['summary']+"\n")
        return output

    def makeEvent(self,departuretime,arrivaltime,code):
        #credentials = getCredentials(code)
        http = self.credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)
        rfcdeparture = time.strftime('%Y-%m-%dT%H:%M:%S',time.gmtime(int(departuretime)/1000))
        rfcarrival = time.strftime('%Y-%m-%dT%H:%M:%S',time.gmtime(int(arrivaltime)))
        print(departuretime)
        print(rfcdeparture)
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
        print(body)
        event = service.events().insert(calendarId='primary',sendNotifications=True, fields="id,start/dateTime", body=body ).execute()
        return(event['id'])

    def updateEvent(eventId,startTime):
        event = service.events().get(calendarId='primary', eventId=eventId).execute()
        event['start']['datetime'] = startTime
        updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
