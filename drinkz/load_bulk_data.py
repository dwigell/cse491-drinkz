"""
Module to load in bulk data from text files.
"""

# ^^ the above is a module-level docstring.  Try:
#
#   import drinkz.load_bulk_data
#   help(drinkz.load_bulk_data)
#

import csv                              # Python csv package

from . import db                        # import from local package

def load_bottle_types(fp):
    """
    Loads in data of the form manufacturer/liquor name/type from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of bottle types loaded
    """
    new_reader = data_reader(fp)
    x = []
    n = 0
    
    while(1):
        try:
            for (mfg, name, typ) in new_reader:
    	    	amt = typ.split()
    	    	#if amt[1] == 'ml' or amt[1] == 'oz':
    	    	if typ.endswith('ml') or typ.endswith('oz'):
    	    	    continue
       	        n += 1
                db.add_bottle_type(mfg, name, typ)
	    new_reader.next()
	except StopIteration:
	    break
    return n

def load_inventory(fp):
    """
    Loads in data of the form manufacturer/liquor name/amount from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of records loaded.

    Note that a LiquorMissing exception is raised if bottle_types_db does
    not contain the manufacturer and liquor name already.
    """
    #reader = csv.reader(fp)
    new_reader = data_reader(fp)

    x = []
    n = 0
 
    while(1):
        try:
    	    for (mfg, name, amount) in new_reader:
    	    	amt = amount.split()
    	    	if amount.endswith('ml') or amount.endswith('oz'):
                    n += 1
                    db.add_to_inventory(mfg, name, amount)
    	    new_reader.next()
    	except StopIteration:
    	    break
    return n
    
    
def data_reader(fp):
    reader = csv.reader(fp)
  
    for line in reader:
	try:
            if line[0].startswith('#'):
		continue
	    if not line[0].strip():
		continue
	    (mfg, name, value) = line
	    yield mfg, name, value
	except IndexError:
            pass
		
		
			
