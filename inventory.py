import json


#method used to add items and categories
def add(body, category):
    db = open('database', mode='r')
    try:
        dbdict = json.loads(db.read())
    except Exception as e:#for when dbdict is empty
        dbdict = dict()
    db.close()
    item = json.loads(body)
    print(item)
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
    elif category != '' and item == '':#adds just a category
        if category in dbdict:
            return({'status':'200 OK','content':'category exists'})#unless that category exists
        else:
            dbdict[category] = {}
    else:#when no item or category is specified
        return({'status':'400 Bad Request','content':'specify category and item'})
    db = open('database', mode='w')
    db.write(json.dumps(dbdict))
    db.close()
    dbjson = printout('', category, None, 0)#gets the current database to return to the client
    return dbjson

#method used to remove items and categories completely
def remove(item, category):
    db = open('database', mode='r')
    try:
        dbdict = json.loads(db.read())
    except Exception as e:
        dbdict = dict()
    db.close()
    if item != '':#checks that an item has been seleceted
        try:
            del dbdict[category][item]
        except Exception:
            return({'status':'400 Bad Request','content':"item does not exist"})
    elif category != '':#checks if only an category has been selected and deletes it all
        try:
            del dbdict[category]
        except Exception:
            return({'status':'400 Bad Request','content':"category does not exist"})
    else:#does not allow for a request to delete at the root directory
        return({'status':'400 Bad Request','content':'deleting the entire database is not allowed'})
    db = open('database', mode='w')
    db.write(json.dumps(dbdict))
    db.close()
    dbjson = printout('','')
    return dbjson


#method used to decrease the quantity of an item
def decrement(item, category, quantity):
    db = open('database', mode='r')
    try:
        dbdict = json.loads(db.read())
    except Exception as e:
        dbdict = dict()
    db.close()
    if dbdict[category][item] >= quantity:#ensures quantity stays positive
        try:
            dbdict[category][item]-=quantity#decreases value of item by specified quantity
        except Exception:
            return({'status':'400 Bad Request','content':'item does not exist'})
        db = open('database', mode='w')
        db.write(json.dumps(dbdict))
        db.close()
        dbjson = printout(item, category)
        return dbjson
    else:
        return({'status':'400 Bad Request','content':'negative quantity error'})

#method used to increment item stock
def increment(item, category, quantity):
    db = open('database', mode='r')
    try:
        dbdict = json.loads(db.read())
    except Exception as e:
        dbdict = dict()
    db.close()
    try:
        dbdict[category][item]+=quantity
    except Exception as E:
        print(format(E))
        return({'status':'400 Bad Request','content':'item does not exist'})
    db = open('database', mode='w')
    db.write(json.dumps(dbdict))
    db.close()
    dbjson = printout(item, category)
    return dbjson

#method used to return all or part of the warehouse database
def printout(item, category, maximum, minimum):
    db = open('database', mode='r')
    try:
        dbjson = json.loads(db.read())
    except Exception as e:
        return({'status':'400 Bad Request','content':'database is empty'})
    db.close()
    if item == '' and category == '' and maximum == None and minimum == 0 :#for returning all items
        return({'status':'200 OK','content':dbjson})
    elif item == '' and maximum == None and minimum == 0:#for returning a selected category
        if category in dbjson:
            return {'status':'200 OK','content':dbjson[category]}
        else:
            return({'status':'400 Bad Request','content':'category not found'})
    elif item != '' and category != '':# returns just an item when requested
        if category in dbjson:
            categorydict = dbjson[category]#in order to check if the item exists in the category the sub-dictionary is extracted
            if item in categorydict:
                return({'status':'200 OK','content':{item:dbjson[category][item]}})
            else:
                return({'status':'400 Bad Request','content':'item not found'})
        else:
            return({'status':'400 Bad Request','content':'category not found'})
    elif maximum != None and minimum >= 0:
        outdict = {}
        if item == '' and category == '':
            for categories in dbjson:
                outdict[categories] = {}
                for items in dbjson[categories]:
                    if dbjson[categories][items] >= minimum and dbjson[categories][items] <= maximum:
                        outdict[categories][items] = dbjson[categories][items]
            return({'status':'200 OK','content':outdict})
        if item == '':
            if category in dbjson:
                for items in dbjson[categories]:
                    if dbjson[categories][items] >= minimum and dbjson[categories][items] <= maximum:
                        outdict[items] = dbjson[categories][items]
                return({'status':'200 OK','content':outdict})
            else:
                return({'status':'404 Not Found','content':'category not found'})
    elif maximum == None and minimum >= 0:
        outdict = {}
        if item == '' and category == '':
            for categories in dbjson:
                for items in dbjson[categories]:
                    if dbjson[categories][items] >= minimum:
                        outdict[items] = dbjson[categories][items]
        if item == '':
            if category in dbjson:
                for items in dbjson[categories]:
                    if dbjson[categories][items] >= minimum:
                        outdict[items] = dbjson[categories][items]
            else:
                return({'status':'404 Not Found','content':'category not found'})
