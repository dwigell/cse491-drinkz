"""
Database functionality for drinkz information.
"""

import convert


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
    fp = open(filename, 'wb')

    tosave = (_bottle_types_db, _inventory_db, _recipe_db)
    dump(tosave, fp)

    fp.close()

def load_db(filename):
    global _bottle_types_db, _inventory_db, _recipe_db
    fp = open(filename, 'rb')

    loaded = load(fp)
    (_bottle_types_db, _inventory_db, _recipe_db) = loaded

    fp.close()

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

