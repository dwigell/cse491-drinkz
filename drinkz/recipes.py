import db
#class for recipes

class Recipe(object):

    def __init__(self, name = "", ingredients = []):
	self.name = name
	self.ingredients = ingredients

    def need_ingredients(self):

        missing_list = []

        # PUT ALL THE LIQUOR TYPES NEEDED IN A LIST(see if they exist) ===========

        bottle_type_list = []
        
	for i in self.ingredients:
	    for item in db._bottle_types_db:
		if  i[0] == item[2]:
		    bottle_type_list.append(item)

        #print bottle_type_list, "bottle_type_list"

        #=========================================================================


        # CHECK INVENTORY FOR THOSE LIQUORS(put them in a list of tuples)=========

        amounts_list = []

	for i in bottle_type_list:
	    if db.check_inventory(i[0], i[1]):
		amount = (i[0], i[2], db.get_liquor_amount(i[0], i[1]))
		amounts_list.append(amount)


        #print amounts_list, "amounts_list"
            
        
        #=========================================================================

        # CREATE THE MISSING LIST=================================================

        
                
        for i in self.ingredients:
            amount = 0.0
            for item in amounts_list: #replace smaller amount with larger
                if i[0]==item[1]:
                    if amount < float(item[2]): 
                        amount = float(item[2])
            ing_amount = db.convert_ml(i[1])#convert the ingredient to ml
            
            if float(amount) < float(ing_amount):#compare the amount with ing
                needed = float(ing_amount)-float(amount)
                needed_tup = (i[0], needed)
                missing_list.append(needed_tup)#add to missing list


	return missing_list
