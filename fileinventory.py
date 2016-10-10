import json
import urllib
from exceptions import *
from inventory import *
import os


class File(Warehouse):
    def __init__(self):
        if not os.path.exists('database'):#this creates the database file as an empty json string if the file does not already exist
            creator = open('database', mode='w')
            creator.write("{}")
            creator.close()

    def load(self):
        db = open('database', mode='r')
        try:
            dbdict = json.loads(db.read())
        except Exception as e:#for when dbdict is empty
            dbdict = dict()
        db.close()
        return dbdict


    def save(self, dbdict, category):
        db = open('database', mode='w')
        db.write(json.dumps(dbdict))
        db.close()
        dbjson = self.printout('', category, None, 0,'')#gets the current database to return to the client
        return dbjson


    #method used to add items and categories
    def add(self,environ):
        body = self.getBody(environ)
        category = self.parseInput(environ)['category']
        dbdict = self.load()
        item = json.loads(body)
        if category != '' and len(item) > 0:#when category and item are specified an item is added
            if category in dbdict:
                for key in item:
                    if item[key] >= 0:
                        dbdict[category][key] = item[key]
                    else:
                        raise NegativeQuantity('quantity must be positive')
                        #return({'status':'400 Bad Request','content':'quantity must be positive'})
            else:
                dbdict[category] = {}#adds category if it doesn't exist
                for key in item:
                    if item[key] >= 0:
                        dbdict[category][key] = item[key]
                    else:
                        raise NegativeQuantity('quantity must be positive')
                        #return({'status':'400 Bad Request','content':'quantity must be positive'})
#        elif category != '' and len(item) == 0:#adds just a category
#            if category in dbdict:
#                return({'status':'200 OK','content':'category exists'})#unless that category exists
#            else:
#                dbdict[category] = {}
#                return self.save(dbdict, category)
        else:#when no item or category is specified
            raise ItemOrCategoryMissing('specify category and item')
            #return({'status':'400 Bad Request','content':'specify category and item'})
        return self.save(dbdict, category)


    #method used to remove items and categories completely
    def remove(self,environ):
        request = self.parseInput(environ)
        item = request['item']
        category = request['category']
        dbdict = self.load()
        if item != '':#checks that an item has been seleceted
            try:
                del dbdict[category][item]
            except Exception:
                raise NotFoundException("item does not exist")
                #return({'status':'404 Not Found','content':"item does not exist"})
        elif category != '':#checks if only an category has been selected and deletes it all
            try:
                del dbdict[category]
                category = ''
            except KeyError:
                raise NotFoundException("category does not exist")
                #return({'status':'404 Not Found','content':"category does not exist"})
        else:#does not allow for a request to delete at the root directory
            raise RootDeleteError('deleting the entire database is not allowed')
            #return({'status':'400 Bad Request','content':'deleting the entire database is not allowed'})
        return self.save(dbdict, category)


    #method used to decrease the quantity of an item
    def decrement(self, item, category, quantity):
        dbdict = self.load()
        try:
            if dbdict[category][item] >= quantity:#ensures quantity stays positive
                dbdict[category][item]-=quantity#decreases value of item by specified quantity
                return self.save(dbdict, category)
        except Exception:
            raise NotFoundException('item does not exist')
            #return({'status':'404 Not Found','content':'item does not exist'})
        else:
            raise NegativeQuantity('negative quantity')
            #return({'status':'400 Bad Request','content':'item does not exist'})


    #method used to increment item stock
    def increment(self, item, category, quantity):
        dbdict = self.load()
        try:
            dbdict[category][item]+=quantity
        except Exception as E:
            print(format(E))
            raise NotFoundException('item does not exist')
            #return({'status':'404 Not Found','content':'item does not exist'})
        return self.save(dbdict, category)


    #method used to return all or part of the warehouse database
    def printout(self, item, category, maximum, minimum, prefix):
        #print(item + ', ' + category)
        dbjson = self.load()
        if item == '' and category == '' and maximum == None and minimum == 0 :#for returning all items
            return({'status':'200 OK','content':json.dumps(dbjson)})
        elif item == '' and category != '' and maximum == None and minimum == 0:#for returning a selected category
            if category in dbjson:
                return {'status':'200 OK','content':json.dumps({category:dbjson[category]})}
            else:
                raise NotFoundException('category not found')
                #return({'status':'404 Not Found','content':'category not found'})
        elif item != '' and category != '':# returns just an item when requested
            print('specific item requested')
            if category in dbjson:
                categorydict = dbjson[category]#in order to check if the item exists in the category the sub-dictionary is extracted
                if item in categorydict:
                    return({'status':'200 OK','content':json.dumps({category:{item:dbjson[category][item]}})})
                else:
                    raise NotFoundException('item not found')
                    #return({'status':'404 Not Found','content':'item not found'})
            else:
                raise NotFoundException('category not found')
                #return({'status':'404 Not Found','content':'category not found'})
        elif maximum != None and minimum >= 0:
            outdict = {}
            if item == '' and category == '':
                for categories in dbjson:
                    for items in dbjson[categories]:
                        if dbjson[categories][items] >= minimum and dbjson[categories][items] <= maximum:
                            outdict[categories] = {}
                            outdict[categories][items] = dbjson[categories][items]
            elif category != '':
                if category in dbjson:
                    for items in dbjson[category]:
                        if dbjson[category][items] >= minimum and dbjson[categories][items] <= maximum:
                            outdict[items] = dbjson[categories][items]
                else:
                    raise NotFoundException('category not found')
                    #return({'status':'404 Not Found','content':'category not found'})
            return({'status':'200 OK','content':json.dumps(outdict)})
        elif maximum == None and minimum >= 0:
            outdict = {}
            if item == '' and category == '':
                for categories in dbjson:
                    for items in dbjson[categories]:
                        if dbjson[categories][items] >= minimum:
                            if categories in outdict:
                                outdict[categories][items] = dbjson[categories][items]
                            else:
                                outdict[categories] = {}
                                outdict[categories][items] = dbjson[categories][items]
            elif item == '' and category != '':
                if category in dbjson:
                    for items in dbjson[categories]:
                        if dbjson[categories][items] >= minimum:
                            outdict[items] = dbjson[categories][items]
                else:
                    raise NotFoundException('category not found')
                    #return({'status':'404 Not Found','content':'category not found'})
            else:
                for categories in dbjson:
                    for items in dbjson[categories]:
                        if dbjson[categories][items] >= minimum:
                            outdict[items] = dbjson[categories][items]
            return({'status':'200 OK','content':json.dumps(outdict)})
