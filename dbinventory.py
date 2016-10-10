import json
import urllib
from exceptions import *
from inventory import *
import sqlite3

class Database(Warehouse):
    def __init__(self):
        pass

    def load(self):#connects to the sqlite database file, creates a table and returns a cursor
        database = sqlite3.connect("items", isolation_level=None)
        cursor = database.cursor()
        cursor.execute("create table if not exists items (name TEXT, quantity INTEGER, category TEXT)")
        return cursor

    def save(self, dbdict, category):#only exists as a placeholder
        pass

    def checkExistence(self, item, category, cursor):
        #checks for an items existence and returns true if it exists, if no item is specified it checks if the specified category exists
        if item == '':
            #checks if a category exists
            command = "select * from items where category = ?"
            cursor.execute(command,(category,))
        else:
            #checks if an item exists
            print('item and category selected')
            command = "select * from items where name = ? and category = ?"
            cursor.execute(command,(item,category))
        results = cursor.fetchall()#gets all of the results from either above operation
        if len(results) > 0:#returns true if the search gave results
            return True
        else:
            return False

    #method used to add items and categories
    def add(self,environ):#adds items to the database
        cursor = self.load()
        body = self.getBody(environ)#gets bady from environ
        category = self.parseInput(environ)['category']#gets the category variable using the abstract classes method
        items = json.loads(body)#takes body and creates a dictionary
        if category != '' and len(items) > 0:#when category and item are specified an item is added
            for item in items:#iterates through the inputs
                quantity = items[item]
                if self.checkExistence(item,category,cursor):#checks if the item already exists
                    command = "update items set quantity = ? where name = ? and category = ?"
                    if quantity >= 0:#check that quantity is positive
                        cursor.execute(command,(quantity,item,category))
                    else:
                        raise NegativeQuantity
                else:#when the item is a new item
                    command = "insert into items values (?,?,?)"
                    if quantity >= 0:
                        cursor.execute(command,(item,quantity,category))
                    else:
                        raise NegativeQuantity
        else:#raises an exception when the item or category has been excluded
            raise ItemOrCategoryMissing
        return self.printout('',category,None,0,'')#returns the modified category

    #method used to remove items and categories completely
    def remove(self,environ):
        cursor = self.load()
        request = self.parseInput(environ)#uses the abstract classes method to get variables
        item = request['item']
        category = request['category']
        if category == '': #category must be specified, deletion of root not allowed
            raise ItemOrCategoryMissing
        else:
            if item == '':#removes a category if no item specified
                if self.checkExistence('',category,cursor):#verifies category
                    command = "delete from items where category = ?"
                    cursor.execute(command, (category,))
                else:
                    raise NotFoundException
            else:#removes a specific item
                print('item removal requested')
                if self.checkExistence(item, category, cursor):#verifies existence of item
                    print('item exists')
                    command = "delete from items where name = ?"
                    cursor.execute(command, (item,))
                else:
                    raise NotFoundException
        return self.printout('','',None,0,'')

    #method used to decrease the quantity of an item, the abstract class parses input and selects decrement vs increment in changeQuantity()
    def decrement(self, item, category, quantity):
        cursor = self.load()
        if self.checkExistence(item, category, cursor):#verifies existence of requested item
            command = "select quantity from items where name = ? and category = ?"
            cursor.execute(command,(item,category))
            number = cursor.fetchone()#gets the quantity of the item to be decremented
            if number[0] >= quantity:#verifies that it will stay positive
                command = "update items set quantity = quantity - ? where name = ? and category = ?"
                cursor.execute(command,(quantity,item,category))
            else:
                raise NegativeQuantity
        else:
            raise NotFoundException
        return self.printout(item,category,None,0,'')#returns the item with its new quantity

    #method used to increase the quantity of an item, the abstract class parses input and selects decrement vs increment in changeQuantity()
    def increment(self, item, category, quantity):
        cursor = self.load()
        if self.checkExistence(item, category, cursor):#verifies existence of requested item
            command = "update items set quantity = quantity + ? where name = ? and category = ?"
            cursor.execute(command,(quantity,item,category))
        else:
            raise NotFoundException
        return self.printout(item,category,None,0,'')#returns the item with its new quantity

    #method used to return all or part of the warehouse database
    def printout(self, item, category, maximum, minimum, prefix):
        cursor = self.load()
        outdict = {}#empty dictionary to be populated by output
        if item == '':#when item is not specified category is checked
            if category == '':#when category is not specified we look for bounds
                if maximum == None and minimum == 0:
                    #return entire databse if no bounds specified
                    command = "select * from items"
                    cursor.execute(command)
                elif maximum == None:
                    #minimum bound specified
                    command = "select * from items where quantity >= ?"
                    cursor.execute(command,(minimum,))
                else:
                    #min and max bound, works with no minimum as well
                    print('min max or no min')
                    command = "select * from items where quantity >= ? and quantity <= ?"
                    cursor.execute(command,(minimum,maximum))
            elif self.checkExistence('',category,cursor):#checks that the category is real when specified
                if maximum == None and minimum == 0:
                    #return entire category
                    print('no bounds')
                    command = "select * from items where category = ?"
                    cursor.execute(command,(category,))
                elif maximum == None:
                    #return category with minimum bound
                    print('minimum bound')
                    command = "select * from items where category = ? and quantity >= ?"
                    cursor.execute(command,(category,minimum))
                else:
                    #return category with min and max bound, works with no minimum as well
                    print('min and max or no min')
                    command = "select * from items where category = ? and quantity >= ? and quantity <= ?"
                    cursor.execute(command,(category,minimum,maximum))
            else:#if the requested category does not exist
                raise NotFoundException
        elif self.checkExistence(item,category,cursor):#checks that specified item exists
            #return requested item
            command = "select * from items where name = ?"
            print(item)
            cursor.execute(command, (item,))
        else:#if prefix was specified, the search is done
            if prefix:
                command = "select * from items where name like ?"
                cursor.execute(command, (item+'%',))
            else:
                raise NotFoundException
        for row in cursor:#builds the output dictionary
            returnedlist = row
            if returnedlist[2] in outdict:#when the category is already in the dictionary add a new item:quantity pair to the category
                outdict[returnedlist[2]][returnedlist[0]] = returnedlist[1]
            else:#if the category hasn't been added yet, add it and put in the first tuple
                outdict[returnedlist[2]] = {}
                outdict[returnedlist[2]] = {returnedlist[0]:returnedlist[1]}
        return{'status':'200 OK','content':json.dumps(outdict)}#converts the output to json to be decoded by the client
