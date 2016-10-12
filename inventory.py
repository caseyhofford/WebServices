import json
import urllib
from exceptions import *
import abc
import base64

class Warehouse(metaclass = abc.ABCMeta):
    def getBody(self,environ):#returns a dictionary of the HTTP body
        if int(environ['CONTENT_LENGTH']) > 0:
            contentlength = int(environ['CONTENT_LENGTH'])
            return environ['wsgi.input'].read(contentlength).decode('utf-8')
        else:
            return '{}'

    #extracts
    def parseInput(self,environ):
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
        if 'option' in querystring and item != '':
            option = querystring['option'][0]
        else:
            option = ''
        if 'prefix' in querystring:
            if querystring['prefix'][0] == 'true':
                prefix = True
            elif querystring['prefix'][0] == 'false':
                prefix = False
            else:
                prefix = ''
        else:
            prefix = ''
        return ({'category':category,'item':item,'quantity':quantity,'maximum':maximum,'minimum':minimum,'option':option, 'prefix':prefix})


    def changeQuantity(self,environ):#determines if increment or decrement was chosen
        request = self.parseInput(environ)
        if request['item'] == '':#prevents user from excluding item
            raise ItemOrCategoryMissing('Please specify an item')
        if request['option'] == 'increment':
            return self.increment(request['item'],request['category'],request['quantity'])
        elif request['option'] == 'decrement':
            return self.decrement(request['item'],request['category'],request['quantity'])
        else:#if something other than increment or decrement is chosen, an error is raised
            raise OptionIncorrect

    def prePrintProcessing(self,environ):#allows the printout method to be called by all other methods for returning desired json objects
        if 'HTTP_AUTHORIZATION' in environ:
            parts = [ x for x in environ['HTTP_AUTHORIZATION'].split(' ') if x.strip() ]
            assert parts[0] == 'Basic'
            authentication = base64.b64decode(parts[1]).decode()
            if authentication == 'casey:password':
                request = self.parseInput(environ)
                item = request['item']
                category = request['category']
                maximum = request['maximum']
                minimum = request['minimum']
                prefix = request['prefix']
                return self.printout(item, category, maximum, minimum, prefix)
            else:
                raise AuthenticationError
        else:
            raise AuthenticationError


    #method used to add items and categories
    @abc.abstractmethod
    def load(self):
        return

    def save(self):
        return

    def add(self,environ):
        return

    #method used to remove items and categories completely
    @abc.abstractmethod
    def remove(self,environ):
        return

    #method used to decrease the quantity of an item
    @abc.abstractmethod
    def decrement(self, item, category, quantity):
        return

    #method used to increment item stock
    @abc.abstractmethod
    def increment(self, item, category, quantity):
        return

    #method used to return all or part of the warehouse database
    @abc.abstractmethod
    def printout(self, item, category, maximum, minimum, prefix):
        return
