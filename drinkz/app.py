#! /usr/bin/env python
from wsgiref.simple_server import make_server
import urlparse
import simplejson

import db, recipes, convert

#=========================

#db.add_bottle_type('Johnnie Walker', 'black label', 'blended scotch')
#db.add_to_inventory('Johnnie Walker', 'black label', '500 ml')

#db.add_bottle_type('Uncle Herman\'s', 'moonshine', 'blended scotch')
#db.add_to_inventory('Uncle Herman\'s', 'moonshine', '5 liter')
        
#db.add_bottle_type('Gray Goose', 'vodka', 'unflavored vodka')
#db.add_to_inventory('Gray Goose', 'vodka', '1 liter')

#db.add_bottle_type('Rossi', 'extra dry vermouth', 'vermouth')
#db.add_to_inventory('Rossi', 'extra dry vermouth', '24 oz')

#r = recipes.Recipe('scotch on the rocks', [('blended scotch', '4 oz')])
#db.add_recipe(r)

#r2 = recipes.Recipe('vomit inducing martini', [('orange juice', '6 oz'), ('vermouth', '1.5 oz')])
#db.add_recipe(r2)

#r3 = recipes.Recipe('whiskey bath', [('blended scotch', '6 liter')])
#db.add_recipe(r3)

#==================================

#filename = "bin/test_database"

#db.load_db(filename)


dispatch = {
    '/' : 'index',
    '/content' : 'somefile',
    '/error' : 'error',
    '/helmet' : 'helmet',
    '/form' : 'form',
    '/recv' : 'recv',
    '/rpc'  : 'dispatch_rpc',

    '/recipes' : 'recipes',
    '/inventory' : 'inventory',
    '/liquorTypes' : 'liquorTypes'
}

html_headers = [('Content-type', 'text/html')]

class SimpleApp(object):
    def __call__(self, environ, start_response):

        path = environ['PATH_INFO']
        fn_name = dispatch.get(path, 'error')

        # retrieve 'self.fn_name' where 'fn_name' is the
        # value in the 'dispatch' dictionary corresponding to
        # the 'path'.
        fn = getattr(self, fn_name, None)

        if fn is None:
            start_response("404 Not Found", html_headers)
            return ["No path %s found" % path]

        return fn(environ, start_response)
            
    def index(self, environ, start_response):
        data = """
<html>
<head>
<title>CSE491</title>
<style type='text/css'>
h1 {color:red;}
body {font-size: 18px;}
</style>
<script>
function alertBox()
{
alert("This is an alert box");
}
</script>
</head>
<body>

<b><h1>Home</h1></b><p>

<a href='form'>Covert to ml</a>
<p>
<a href='recipes'>Recipes</a>
<p>
<a href='inventory'>Inventory</a>
<p>
<a href='liquorTypes'>Liquor Types</a>
<p>
<input type="button" onclick="alertBox()" value="Show alert box" />

</body>
</html>
"""
        start_response('200 OK', list(html_headers))
        return [data]

#======================================================= RECIPES
    def recipes(self, environ, start_response):

        data = """
<html>
<head>
<title>CSE491-Recipes</title>
<style type = 'text/css'>
h1 {color:green;}
body {font-size: 18px;}
</style>
</head>
<body>
"""
        data += "<b><h1>Recipes</h1></b><p>Recipe, Do We Have All the Ingredients?</p><ul>"

        for key in db._recipe_db:
            a = db._recipe_db[key].ingredients[0][0]
            b = db._recipe_db[key].ingredients[0][1]
            if len(db._recipe_db[key].need_ingredients())>0:
                answer = "No"
                data += """<p></p><li> %s, %s, %s, <b> %s</b><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS_-xqzPnoj6Fv6aT7JeoZl7B_QsnwcfrdhuhyeZIS5SW0RutbRAg" alt="sad" width="50" height="50">""" % (key, a, b, answer)
            else:
                answer = "Yes"
                data += """<p></p><li> %s, %s, %s, <b> %s</b><img src="https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcROxLShuNusDhjtK3yGGl0wT5MFKK521IWA34D8JCnTDw5Bb0fBsg" alt="happy" width="50" height="50">""" % (key, a, b, answer)

        data += "</ul>"

        data += """
<p><a href='/'>Home</a>
</p>
<p><a href='inventory'>Inventory</a>
</p>
<p><a href='liquorTypes'>Liquor Types</a>
</p>
</body>
</html>
"""

        start_response('200 OK', list(html_headers))
        return [data]
#************************************************************* INVENTORY
    def inventory(self, environ, start_response):

        data = """
<html>
<head>
<title>CSE491-Inventory</title>
<style type = 'text/css'>
h1 {color:green;}
body {font-size: 18px;}
</style>
</head>
<body>
"""
        
        data += "<b><h1>Inventory</h1></b><p>Manufacturer, Liquor Type, Amount (ml)</p><ul>"

        for mfg, liquor in db.get_liquor_inventory():
            data += "<p> </p>"
            data += "<li> %s,  %s, %s" % (mfg, liquor, db.get_liquor_amount(mfg,liquor))

        data += "</ul>"

        data += """
<p><a href='/'>Home</a>
</p>
<p><a href='recipes'>Recipes</a>
</p>
<p><a href='liquorTypes'>Liquor Types</a>
</p>
</body>
</html>
"""
        start_response('200 OK', list(html_headers))
        return [data]

#************************************************************ LIQUOR TYPES

    def liquorTypes(self, environ, start_response):

        data = """
<html>
<head>
<title>CSE491-Liquor-Types</title>
<style type = 'text/css'>
h1 {color:green;}
body {font-size: 18px;}
</style>
</head>
<body>
"""
        
        data += "<b><h1>Liquor Types</h1></b><p>Manufacturer, Liquor Type</p><ul>"

        for mfg, liquor in db.get_liquor_inventory():
            data += "<p> </p>"
            data += '<li> %s, %s' % (mfg, liquor)

        data += "</ul>"

        data += """
<p><a href='/'>Home</a>
</p>
<p><a href='recipes'>Recipes</a>
</p>
<p><a href='inventory'>Inventory</a>
</p>
</body>
</html>
"""
        start_response('200 OK', list(html_headers))
        return [data]

#=======================================================
        
    def somefile(self, environ, start_response):
        content_type = 'text/html'
        data = open('somefile.html').read()

        start_response('200 OK', list(html_headers))
        return [data]

    def error(self, environ, start_response):
        status = "404 Not Found"
        content_type = 'text/html'
        data = "Couldn't find your stuff."
       
        start_response('200 OK', list(html_headers))
        return [data]

    def helmet(self, environ, start_response):
        content_type = 'image/gif'
        data = open('Spartan-helmet-Black-150-pxls.gif', 'rb').read()

        start_response('200 OK', [('Content-type', content_type)])
        return [data]

    def form(self, environ, start_response):
        data = form()

        start_response('200 OK', list(html_headers))
        return [data]
   
    def recv(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        amount = results['amount'][0]

        amount_ml = convert.convert_ml(amount)

        content_type = 'text/html'
        data = "Amount in ml: %d <a href='/'>return to index</a>" % (amount_ml)

        start_response('200 OK', list(html_headers))
        return [data]

    def dispatch_rpc(self, environ, start_response):
        # POST requests deliver input data via a file-like handle,
        # with the size of the data specified by CONTENT_LENGTH;
        # see the WSGI PEP.
        
        if environ['REQUEST_METHOD'].endswith('POST'):
            body = None
            if environ.get('CONTENT_LENGTH'):
                length = int(environ['CONTENT_LENGTH'])
                body = environ['wsgi.input'].read(length)
                response = self._dispatch(body) + '\n'
                start_response('200 OK', [('Content-Type', 'application/json')])

                return [response]

        # default to a non JSON-RPC error.
        status = "404 Not Found"
        content_type = 'text/html'
        data = "Couldn't find your stuff."
       
        start_response('200 OK', list(html_headers))
        return [data]

    def _decode(self, json):
        return simplejson.loads(json)

    def _dispatch(self, json):
        rpc_request = self._decode(json)

        method = rpc_request['method']
        params = rpc_request['params']
        
        rpc_fn_name = 'rpc_' + method
        fn = getattr(self, rpc_fn_name)
        result = fn(*params)

        response = { 'result' : result, 'error' : None, 'id' : 1 }
        response = simplejson.dumps(response)
        return str(response)

    def rpc_hello(self):
        return 'world!'

    def rpc_add(self, a, b):
        return int(a) + int(b)

#==========================================
    def rpc_convert_units_to_ml(self, amount):
        amt = convert.convert_ml(amount)
        return amt

    def rpc_get_recipe_names(self):
        names = db.get_all_recipe_names()
        return names

    def rpc_get_liquor_inventory(self):
        inventory = db.get_liquor_inventory()
        return inventory
#===========================================
    
def form():
    return """
<form action='recv'>
Amount(Please include units)<p></p> <input type='text' name='amount' size'20'>
<input type='submit'>
</form>
"""

if __name__ == '__main__':
    import random, socket
    port = random.randint(8000, 9999)
    
    app = SimpleApp()
    
    httpd = make_server('', port, app)
    print "Serving on port %d..." % port
    print "Try using a Web browser to go to http://%s:%d/" % \
          (socket.getfqdn(), port)
    httpd.serve_forever()
