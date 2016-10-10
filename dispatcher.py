#!/usr/bin/python3
import pprint
import json
from fileinventory import *
from dbinventory import *
import urllib.parse

def processRequest(environ,storage):
    if storage == 'files':
        resource = File()
    elif storage == 'database':
        resource = Database()
    else:
        raise OptionIncorrect()
    method = environ['REQUEST_METHOD']#takes method from environ passed by server
    if method == 'GET':#GET will return the requested portion of the warehouse data
        return resource.prePrintProcessing(environ)
    elif method == 'POST':#POST will return the added item and quantity
        return resource.add(environ)
    elif method == 'PUT':#PUT can increment or decrement as specified in the option parameter of the query string
        return resource.changeQuantity(environ)
    elif method == 'DELETE':#this removes the selected item and returns the whole database
        return resource.remove(environ)
    else:#no other HTTP methods are allowed
        return({'status':'400 Bad Request','content':'Specified method "' + method + '" is not valid'})
