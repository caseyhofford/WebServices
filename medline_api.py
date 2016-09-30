#!/usr/bin/env python3
from pprint import pprint
import http.client, urllib.parse
import xml.etree.ElementTree as ET
def http_get(connection, path):
    connection.request('GET', path)
    response = connection.getresponse()
    if response.status == 200:
        #when the server returns a document
        xmldata = ET.parse(response) #takes the xml file and creates an ElementTree
        count = xmldata.find("count") #gives total results available
        totres = int(count.text)
        retmax = xmldata.find("retmax") #gives # of results being displayed
        dispres = int(retmax.text)
        print(str(totres) + " results found. Displaying the first " + str(dispres) + " results")
        links = list(xmldata.iter("document")) #creates a list of elements with the document tag
        for i in links:
            print(i.get("rank") + ": " + i.get("url")) #prints desired elements from the list 'links'
        return xmldata #unnecessary but would make it easier to process the xml further as in a larger application
    else:
        raise Exception("HTTP call failed: " + response.reason)

#def process_xml(xmldata):


url = 'wsearch.nlm.nih.gov'
search = input('What would you like to search for? ')
results = input('How many results would you like to display? ')
while results.isdigit() != True:
    print ("That wasn't a number silly!")
    results = input('How many results would you like to display? ')
search.replace(" ", "+")#formats query for URI
connection = http.client.HTTPSConnection(url)
output = http_get(connection, '/ws/query?db=healthTopics&term='+ search + '&retmax=' + results)
