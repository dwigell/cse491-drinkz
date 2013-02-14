"""
Database functionality for drinkz information.
"""

# private singleton variables at module level
_bottle_types_db = set(tuple())
_inventory_db = {}

def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db
    _bottle_types_db = set(tuple())
    _inventory_db = {}

# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
class LiquorMissing(Exception):
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
	item = amount.split()
	if item[1]=="oz":
	    new_amount = convert_oz(amount)#FLOAT AMOUNT
            old_amount = (get_liquor_amount(mfg, liquor)).split()
       	    old_amount_float = old_amount[0]#FLOAT OLD AMOUNT
            new_total = float(old_amount_float) + float(new_amount)
	    _inventory_db[(mfg, liquor)] = repr(new_total)+' ml'

	if item[1]=="ml":
	    new_amount = item[0]
	    old_amount = (get_liquor_amount(mfg, liquor)).split()
            old_amount_float = old_amount[0]
	    new_total = float(old_amount_float) + float(new_amount)
	    _inventory_db[(mfg, liquor)] = repr(new_total)+' ml'	
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
    
    for item in amounts:
        item_amount = item.split()
        if item_amount[1]=="oz":
            total_ml += float(item_amount[0]) * 29.5735
        else:
            total_ml += float(item_amount[0])
    
	total = repr(total_ml) + ' ml'    

    return total 

def get_liquor_inventory(): 
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for key in _inventory_db:
        yield key[0], key[1]

def convert_oz(amount):
    total = 0.0

    item = amount.split()
    if item[1]=="oz":
	total += float(item[0]) * 29.5735
    return total        
