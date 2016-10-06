#!/usr/bin/python3
import pprint
import json
from inventory import *
import urllib.parse
import os

def processRequest(environ):
    if not os.path.exists('database'):#this creates the database file as an empty json string if the file does not already exist
        creator = open('database', mode='w')
        creator.write("{}")
        creator.close()
    method = environ['REQUEST_METHOD']#takes method from environ passed by server
    path = environ['PATH_INFO']#takes path from environ
    patharray = path.split('/')#creates an array of the path hierarchy
    items = {}
    if '' in patharray:#removes the preceding empty string of the root path
        patharray.remove('')
    if len(patharray) > 2:#there are only two levels of resources allowed
        return {'status':'400 Bad Request','content':"Path too long"}
    elif len(patharray) == 2:
        category = patharray[0]
        item = patharray[1]
    elif len(patharray) == 1:# when only one level is specified, it must be the category
        category = patharray[0]
        item = ''
    else:#if nothing is specified, both are empy
        category = ''
        item = ''

    querystring = urllib.parse.parse_qs(environ['QUERY_STRING'])#creates a dictionary of query parameters
    if 'quant' in querystring:
        quantity = int(querystring['quant'][0])#0th index needed due to formatting of parse_qs as key:list pairs
    else:
        quantity = 0#default quantity as specified in the API
    if 'max' in querystring:
        maximum = int(querystring['max'][0])
    else:
        maximum = None
    if 'min' in querystring:
        minimum = int(querystring['min'][0])
    else:
        minimum = 0

    if environ['CONTENT_LENGTH'] != '':
        contentlength = int(environ['CONTENT_LENGTH'])
        content = environ['wsgi.input'].read(contentlength).decode('utf-8')
    else:
        contentlength = 0
        content = ""

    if method == 'GET':#GET will return the requested portion of the warehouse data
        return printout(item, category, maximum, minimum)
    elif method == 'POST':#POST will return the added item and quantity
        return add(content, category)
    elif method == 'PUT':#PUT can increment or decrement as specified in the option parameter of the query string
        if 'option' in querystring and item != '':
            if querystring['option'][0] == 'increment':
                return increment(item, category, quantity)
            elif querystring['option'][0] == 'decrement':
                return decrement(item, category, quantity)
            else:
                return({'status':'400 Bad Request','content':'invalid option, choose increment or decrement'})
        else:
            return({'status':'400 Bad Request','content':'plese include the option parameter in your query string and a path to an item, not a category'})
    elif method == 'DELETE':#this removes the selected item and returns the whole database
        return(remove(item, category))
    else:#no other HTTP methods are allowed
        return({'status':'400 Bad Request','content':'Specified method "' + method + '" is not valid'})
