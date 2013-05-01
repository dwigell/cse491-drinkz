"""
Database functionality for drinkz information.
"""

import convert

import sqlite3, os
import os
import sys
import recipes

from cPickle import dump, load


# private singleton variables at module level
_bottle_types_db = set(tuple())
_inventory_db = {}

_recipe_db = {}

def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db, _recipe_db
    _bottle_types_db = set(tuple())
    _inventory_db = {}
    _recipe_db = {}

def save_db(filename):

    try:
        os.unlink(filename)
    except OSError:
        pass

    db = sqlite3.connect(filename)

    with db:
        c = db.cursor()

        c.execute("CREATE TABLE BottleTypes(mfg STRING, liquor STRING, typ STRING)")
        c.execute("CREATE TABLE Inventory(mfg STRING, liquor STRING, amount STRING)")
        c.execute("CREATE TABLE Recipes(name STRING, ingredients BUFFER)")


        for (m, l, typ) in _bottle_types_db:
            c.execute("insert into BottleTypes values (?, ?, ?)", (m, l, typ))
        for (m, l) in _inventory_db:
            mfg = m
            liquor = l
            amount = _inventory_db[(mfg, liquor)]
            c.execute("insert into Inventory values (?, ?, ?)", (mfg, liquor, amount))

        for key in _recipe_db:
            templist = _recipe_db[key].ingredients # ingredients list
            buflist = buffer(convert_list_to_str(templist)) # convert ingredients to string
            c.execute("insert into Recipes values (?, ?)", (key, buflist)) # insert into db

        db.commit()
        c.close()


#==========================================================
#    fp = open(filename, 'wb')
#
#    tosave = (_bottle_types_db, _inventory_db, _recipe_db)
#    dump(tosave, fp)
#
#    fp.close()
#==========================================================







def load_db(filename):

    db = sqlite3.connect(filename)
    db.text_factory = str

    with db:

        c = db.cursor()

        c.execute("SELECT * FROM BottleTypes") # put all bottletypes into db
        rows = c.fetchall()
        for row in rows:
            mfg,liquor,typ = row
            
            _bottle_types_db.add((mfg,liquor,typ))

        c.execute("SELECT * FROM Inventory") # put all inventory items into db
        rows = c.fetchall()
        for row in rows:
            mfg,liquor,amt = row
            _inventory_db[(mfg, liquor)]=amt

        c.execute("SELECT * FROM Recipes") # put all recipes into db
        rows = c.fetchall()
        for row in rows:
            name,ingredients = row

            ing_list = convert_str_to_list(str(ingredients))# convert ingredients back to list of tuples
            
            r = recipes.Recipe(name,ing_list) #create recipe object
            add_recipe(r) #add to database

        db.commit()
        c.close()

        
        

#===================================================================
#    global _bottle_types_db, _inventory_db, _recipe_db
#    fp = open(filename, 'rb')
#
#    loaded = load(fp)
#    (_bottle_types_db, _inventory_db, _recipe_db) = loaded
#
#    fp.close()
#
#===================================================================



# convert a list to a string(ingredients list to string)
def convert_list_to_str(l):
    slist = ""

    for item in l:
        #items in l are tuples of two: (liquor, amt)
        liquor, amt = item

        slist += "{}:{};".format(liquor, amt)
    return slist[:-1]

#convert the string back to list
def convert_str_to_list(s):
    regular_list = []

    for t in s.split(';'): #use the ; symbol to separate the tuples
        liq, amt = t.split(':') # split the tup into its proper values
        regular_list.append((liq, amt)) # append the tup to the list

    return regular_list
    
# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
class LiquorMissing(Exception):
    pass
class DuplicateRecipeName(Exception):
    pass

def add_bottle_type(mfg, liquor, typ):
    "Add the given bottle type into the drinkz database."
    _bottle_types_db.add((mfg, liquor, typ))

def _check_bottle_type_exists(mfg, liquor):
    for (m, l, _) in _bottle_types_db:
        if mfg == m and liquor == l:
            return True

    return False

def add_to_inventory(mfg, liquor, amount):
    "Add the given liquor/amount to inventory."
    if not _check_bottle_type_exists(mfg, liquor):
        err = "Missing liquor: manufacturer '%s', name '%s'" % (mfg, liquor)
        raise LiquorMissing(err)

    # SINCE INVENTORY IS A DICT, CHECK INVENTORY FOR LIQUOR
    # AND ADD INVENTORY AMOUNT WITH NEW AMOUNT  

    if check_inventory(mfg, liquor):
	
        new_amount = convert.convert_ml(amount)#FLOAT AMOUNT
        old_amount = get_liquor_amount(mfg, liquor)
        new_total = float(old_amount) + float(new_amount)
        _inventory_db[(mfg, liquor)] = str(new_total)+' ml'


    else:    
    # ADD/UPDATE INVENTORY ITEM
        _inventory_db[(mfg, liquor)] =  amount

def check_inventory(mfg, liquor):
    for key in _inventory_db:
        if mfg == key[0] and liquor == key[1]:
            return True
        
    return False

def get_liquor_amount(mfg, liquor):
    "Retrieve the total amount of any given liquor currently in inventory."
    amounts = []
    for key in _inventory_db:
        if mfg == key[0] and liquor == key[1]:
           amounts.append(_inventory_db[key])
            
    total_ml = 0.0

    for i in amounts:
        total_ml += float(convert.convert_ml(i))    

    return total_ml 

def get_liquor_inventory(): 
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for key in _inventory_db:
        yield key[0], key[1]


def add_recipe(r):
    
    if r.name not in _recipe_db:
        _recipe_db[r.name]=r
    else:
        raise DuplicateRecipeName()
    
def get_recipe(name):
    if name not in _recipe_db:
	return None
    return _recipe_db[name]

def get_all_recipes():
    
    return _recipe_db.values()

def get_all_recipe_names():
    return _recipe_db.keys()

