import app
import urllib
import db
import recipes

def test_app_recipes():

    r = recipes.Recipe('scotch on the rocks', [('blended scotch', '4 oz')])
    db.add_recipe(r)

    r2 = recipes.Recipe('vomit inducing martini', [('orange juice', '6 oz'), ('vermouth', '1.5 oz')])
    db.add_recipe(r2)

    r3 = recipes.Recipe('whiskey bath', [('blended scotch', '6 liter')])
    db.add_recipe(r3)

    environ = {}
    environ['PATH_INFO'] = '/recipes'

    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    app_obj = app.SimpleApp()
    results = app_obj(environ, my_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']

    assert text.find('scotch on the rocks') != -1, text
    assert text.find('vomit inducing martini') != -1, text
    assert text.find('whiskey bath') != -1, text
    assert ('Content-type', 'text/html') in headers
    assert status == '200 OK'
