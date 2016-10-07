import json


def getBody(environ):
    if int(environ['CONTENT_LENGTH']) > 0:
        contentlength = int(environ['CONTENT_LENGTH'])
        return environ['wsgi.input'].read(contentlength).decode('utf-8')
    else:
        return '{}'

def load():
    db = open('database', mode='r')
    try:
        dbdict = json.loads(db.read())
    except Exception as e:#for when dbdict is empty
        dbdict = dict()
    db.close()
    return dbdict

def save(dbdict, category):
    db = open('database', mode='w')
    db.write(json.dumps(dbdict))
    db.close()
    dbjson = printout('', category, None, 0)#gets the current database to return to the client
    return dbjson

#method used to add items and categories
def add(category, environ):
    body = getBody(environ)
    dbdict = load()
    item = json.loads(body)
    if category != '' and len(item) > 0:#when category and item are specified an item is added
        if category in dbdict:
            for key in item:
                if item[key] >= 0:
                    dbdict[category][key] = item[key]
                else:
                    return({'status':'400 Bad Request','content':'quantity must be positive'})
        else:
            dbdict[category] = {}#adds category if it doesn't exist
            for key in item:
                if item[key] >= 0:
                    dbdict[category][key] = item[key]
                else:
                    return({'status':'400 Bad Request','content':'quantity must be positive'})
    elif category != '' and len(item) == 0:#adds just a category
        if category in dbdict:
            return({'status':'200 OK','content':'category exists'})#unless that category exists
        else:
            dbdict[category] = {}
            return save(dbdict, category)
    else:#when no item or category is specified
        return({'status':'400 Bad Request','content':'specify category and item'})
    return save(dbdict, category)

#method used to remove items and categories completely
def remove(item, category):
    dbdict = load()
    if item != '':#checks that an item has been seleceted
        try:
            del dbdict[category][item]
        except Exception:
            return({'status':'404 Not Found','content':"item does not exist"})
    elif category != '':#checks if only an category has been selected and deletes it all
        try:
            del dbdict[category]
            category = ''
        except KeyError:
            return({'status':'404 Not Found','content':"category does not exist"})
    else:#does not allow for a request to delete at the root directory
        return({'status':'400 Bad Request','content':'deleting the entire database is not allowed'})
    return save(dbdict, category)


#method used to decrease the quantity of an item
def decrement(item, category, quantity):
    dbdict = load()
    try:
        if dbdict[category][item] >= quantity:#ensures quantity stays positive
            dbdict[category][item]-=quantity#decreases value of item by specified quantity
            return save(dbdict, category)
    except Exception:
        return({'status':'404 Not Found','content':'item does not exist'})
    else:
        return({'status':'400 Bad Request','content':'negative quantity error'})

#method used to increment item stock
def increment(item, category, quantity):
    dbdict = load()
    try:
        dbdict[category][item]+=quantity
    except Exception as E:
        print(format(E))
        return({'status':'404 Not Found','content':'item does not exist'})
    return save(dbdict, category)

#method used to return all or part of the warehouse database
def printout(item, category, maximum, minimum):
    #print(item + ', ' + category)
    dbjson = load()
    if item == '' and category == '' and maximum == None and minimum == 0 :#for returning all items
        return({'status':'200 OK','content':dbjson})
    elif item == '' and category != '' and maximum == None and minimum == 0:#for returning a selected category
        if category in dbjson:
            return {'status':'200 OK','content':dbjson[category]}
        else:
            return({'status':'404 Bad Request','content':'category not found'})
    elif item != '' and category != '':# returns just an item when requested
        print('specific item requested')
        if category in dbjson:
            categorydict = dbjson[category]#in order to check if the item exists in the category the sub-dictionary is extracted
            if item in categorydict:
                return({'status':'200 OK','content':{item:dbjson[category][item]}})
            else:
                return({'status':'404 Not Found','content':'item not found'})
        else:
            return({'status':'404 Not Found','content':'category not found'})
    elif maximum != None and minimum >= 0:
        outdict = {}
        if item == '' and category == '':
            for categories in dbjson:
                outdict[categories] = {}
                for items in dbjson[categories]:
                    if dbjson[categories][items] >= minimum and dbjson[categories][items] <= maximum:
                        outdict[categories][items] = dbjson[categories][items]
        elif category != '':
            if category in dbjson:
                for items in dbjson[category]:
                    if dbjson[category][items] >= minimum and dbjson[categories][items] <= maximum:
                        outdict[items] = dbjson[categories][items]
            else:
                return({'status':'404 Not Found','content':'category not found'})
        return({'status':'200 OK','content':outdict})
    elif maximum == None and minimum >= 0:
        outdict = {}
        if item == '' and category == '':
            for categories in dbjson:
                for items in dbjson[categories]:
                    if dbjson[categories][items] >= minimum:
                        outdict[items] = dbjson[categories][items]
        elif item == '' and category != '':
            if category in dbjson:
                for items in dbjson[categories]:
                    if dbjson[categories][items] >= minimum:
                        outdict[items] = dbjson[categories][items]
            else:
                return({'status':'404 Not Found','content':'category not found'})
        else:
            for categories in dbjson:
                for items in dbjson[categories]:
                    if dbjson[categories][items] >= minimum:
                        outdict[items] = dbjson[categories][items]
        return({'status':'200 OK','content':outdict})
