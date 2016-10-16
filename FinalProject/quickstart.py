#import os
from apiclient import discovery
from oauth2client import client
#from oauth2client import tools
#from oauth2client.file import Storage
import datetime
import httplib2


SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'BusNotifier'

#def get_authurl():
#    auth_uri = flow.step1_get_authorize_url()
#    return({'flow':flow,'uri':auth_uri})

def getCredentials(authorization, flow):
    credentials = flow.step2_exchange(authorization)
    return credentials

def getCal(code):
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    output = ''
    flow = client.flow_from_clientsecrets('client_secret.json',scope='https://www.googleapis.com/auth/calendar',redirect_uri='http://127.0.0.2:8000')
    print(code)
    authorization = code
    credentials = getCredentials(authorization, flow)
    http = credentials.authorize(httplib2.Http())
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
