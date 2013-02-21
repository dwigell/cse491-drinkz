#! /usr/bin/env python

import drinkz.db
import drinkz.recipes

drinkz.db.add_bottle_type('Johnnie Walker', 'black label', 'blended scotch')
drinkz.db.add_to_inventory('Johnnie Walker', 'black label', '500 ml')

drinkz.db.add_bottle_type('Uncle Herman\'s', 'moonshine', 'blended scotch')
drinkz.db.add_to_inventory('Uncle Herman\'s', 'moonshine', '5 liter')
        
drinkz.db.add_bottle_type('Gray Goose', 'vodka', 'unflavored vodka')
drinkz.db.add_to_inventory('Gray Goose', 'vodka', '1 liter')

drinkz.db.add_bottle_type('Rossi', 'extra dry vermouth', 'vermouth')
drinkz.db.add_to_inventory('Rossi', 'extra dry vermouth', '24 oz')

r = drinkz.recipes.Recipe('scotch on the rocks', [('blended scotch', '4 oz')])
drinkz.db.add_recipe(r)

r2 = drinkz.recipes.Recipe('vomit inducing martini', [('orange juice', '6 oz'), ('vermouth', '1.5 oz')])
drinkz.db.add_recipe(r2)

r3 = drinkz.recipes.Recipe('whiskey bath', [('blended scotch', '6 liter')])
drinkz.db.add_recipe(r3)


import os

try:
    os.mkdir('html')
except OSError:
    # already exists
    pass


###Index

fp = open('html/index.html', 'w')
print >>fp, "Homework 3 <p><a href='recipes.html'>Recipes</a>"

print >>fp, """
<p>
<a href='inventory.html'>Inventory</a>

</p>
<p>
<a href='liquor_types.html'>Liquor Types</a>
</p>
"""
fp.close()

###Recipes

fp = open('html/recipes.html', 'w')

print >>fp, "<b>Recipes</b><p>Recipe, Ingredients List, Do We Have All the Ingredients?</p><ul>"
 

for key in drinkz.db._recipe_db:
    iList=[]
    for item in drinkz.db._recipe_db.values():
        for i in item.ingredients:
            iList.append(i)
    if len(drinkz.db._recipe_db[key].need_ingredients()) > 0:
        answer = "No"
    else:
        answer = "Yes"
    print >>fp, "<p></p><li> %s, %s,<b> %s</b>" % (key, iList, answer)

print >>fp, "</ul>"


print >>fp, """

<p><a href='index.html'>Back to Index</a>
</p>
<p><a href='inventory.html'>Inventory</a>
</p>
<p><a href='liquor_types.html'>Liquor Types</a>
</p>
"""
fp.close()

###Liquor Types

fp = open('html/liquor_types.html', 'w')


print >>fp, "<b>Liquor Types</b><p>Manufacturer, Liquor Type</p><ul>"

for mfg, liquor in drinkz.db.get_liquor_inventory():
    print >>fp, "<p> </p>"
    print >>fp, '<li> %s, %s' % (mfg, liquor)

print >>fp, "</ul>"

print >>fp, """

<p><a href='index.html'>Back to Index</a>
</p>
<p><a href='recipes.html'>Recipes</a>
</p>
<p><a href='inventory.html'>Inventory</a>
</p>
"""
fp.close()

###Inventory

fp = open('html/inventory.html', 'w')

print >>fp, "<b>Inventory</b><p>Manufacturer, Liquor Type, Amount (ml)</p><ul>"
for mfg, liquor in drinkz.db.get_liquor_inventory():
    #print mfg + "              " + liquor + "          " + drinkz.db.get_liquor_amount(mfg,liquor)
    print >>fp, "<p> </p>"
    print >>fp , "<li> %s,  %s, %s" % (mfg, liquor, drinkz.db.get_liquor_amount(mfg,liquor))
    
print >>fp, "</ul>"

print >>fp, """

<p><a href='index.html'>Back to Index</a>
</p>
<p><a href='recipes.html'>Recipes</a>
</p>
<p><a href='liquor_types.html'>Liquor Types</a>
</p>
"""

fp.close()




