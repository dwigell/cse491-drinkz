import sys
import simplejson
import urllib2
import db, recipes, app
import StringIO
import os
import urlparse

def call_remote(method, params, id):

    app_obj = app.SimpleApp()
    d = dict(method=method, params=params, id=id)
    encoded = simplejson.dumps(d)

    output = StringIO.StringIO(encoded)
    length = len(encoded)


    environ = {}
    environ['PATH_INFO'] = '/rpc'
    environ['REQUEST_METHOD'] = 'POST'
    environ['CONTENT_LENGTH'] = length
    environ['wsgi.input'] = output


    d={}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    results = app_obj(environ, my_start_response)
    

    status, headers = d['status'], d['headers']
    assert ('Content-Type', 'application/json') in headers
    assert status == '200 OK'

    text = "".join(results)
    return text

def test_json_conversion():

    conversion = call_remote(method='convert_units_to_ml', params = ["2 liters"], id='1')

    rpc_request = simplejson.loads(conversion)

    result = rpc_request['result']

    print result

    assert result == 2000

def test_json_recipe_names():
    r = recipes.Recipe('scotch on the rocks', [('blended scotch', '4 oz')])
    db.add_recipe(r)

    r2 = recipes.Recipe('vomit inducing martini', [('orange juice', '6 oz'), ('vermouth', '1.5 oz')])
    db.add_recipe(r2)

    r3 = recipes.Recipe('whiskey bath', [('blended scotch', '6 liter')])
    db.add_recipe(r3)

    recipe_names = call_remote(method='get_recipe_names', params = [], id='1')

    rpc_request = simplejson.loads(recipe_names)

    result = rpc_request['result']

    print result

    assert result == ['scotch on the rocks', 'vomit inducing martini', 'whiskey bath']

def test_json_liquor_inventory():
    db._reset_db()
    db.add_bottle_type('Johnnie Walker', 'black label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'black label', '500 ml')

    db.add_bottle_type('Uncle Herman\'s', 'moonshine', 'blended scotch')
    db.add_to_inventory('Uncle Herman\'s', 'moonshine', '5 liter')
        
    db.add_bottle_type('Gray Goose', 'vodka', 'unflavored vodka')
    db.add_to_inventory('Gray Goose', 'vodka', '1 liter')

    db.add_bottle_type('Rossi', 'extra dry vermouth', 'vermouth')
    db.add_to_inventory('Rossi', 'extra dry vermouth', '24 oz')

    liquor_inventory = call_remote(method='get_liquor_inventory', params = [], id='1')

    rpc_request = simplejson.loads(liquor_inventory)

    result = rpc_request['result']

    
    print result

    assert ['Johnnie Walker', 'black label'] in result
    assert ['Rossi', 'extra dry vermouth'] in result
    assert ["Uncle Herman's", 'moonshine'] in result
    assert ['Gray Goose', 'vodka'] in result

    

    
                
                      
