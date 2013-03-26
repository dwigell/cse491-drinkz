"""
Database functionality for drinkz information.
"""
import convert
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
        _inventory_db[(mfg, liquor)] = repr(new_total)+' ml'

#	if item[1]=="ml":
#	    new_amount = item[0]
#	    old_amount = get_liquor_amount(mfg, liquor)
#	    new_total = float(old_amount) + float(new_amount)
#	    _inventory_db[(mfg, liquor)] = repr(new_total)+' ml'

#	if item[1]=="gallon" or item[1]=="gallons":
#	    new_amount = convert_ml(amount)
#	    old_amount = get_liquor_amount(mfg, liquor)
#	    new_total = float(old_amount) + float(new_amount)
#	    _inventory_db[(mfg, liquor)] = repr(new_total)+' ml'

#       if item[1]=="liter" or item[1]=="liters":
#          new_amount = convert_ml(amount)
#          old_amount = get_liquor_amount(mfg, liquor)
#          new_total = float(old_amount) + float(new_amount)
#          _inventory_db[(mfg, liquor)] = repr(new_total)+' ml'
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
    
#    for item in amounts:
#        item_amount = item.split()
#        if item_amount[1]=="oz":
#            total_ml += float(item_amount[0]) * 29.5735
#	elif item_amount[1]=="gallon" or item_amount[1]=="gallons":
#	    total_ml += float(item_amount[0]) * 3785.41
#        elif item_amount[1]=="liter" or item_amount[1]=="liters":
#            total_ml += float(item_amount[0]) * 1000
#        else:
#            total_ml += float(item_amount[0])    

    return total_ml 

def get_liquor_inventory(): 
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for key in _inventory_db:
        yield key[0], key[1]

def convert_ml(amount):
    total = 0.0

    item = amount.split()
    if item[1]=="oz":
	total += float(item[0]) * 29.5735
    if item[1]=="gallon" or item[1]=="gallons":
        total += float(item[0]) * 3785.41
    if item[1]=="liter" or item[1]=="liters":
        total += float(item[0]) * 1000
    return total

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
