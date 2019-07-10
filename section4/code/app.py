from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'secret' #example only, do not expose in this way on production environments
api = Api(app)
jwt = JWT(app, authenticate, identity) #creates /auth endpoint, takes username and password
                                       #passes the params to the authentication

items = []


class Item(Resource):
    @jwt_required()
    def get(self, name):    #defines the get http method
        #IMPERATIVE SEARCH
        #for item in items:
        #    if item['name'] == name:
        #        return item #FLASK-RESTFUL does not require jsonify
        # FUNCTIONAL VERSION next() returns the first item, error raised if no items left or present
        item = next(filter(lambda x: x['name'] == name, items), None) #else return none
        return {'item': item}, 200 if item is not None else 404 #status codes
        # return is JSON

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': "an item with the name '{}' already exists.".format(name)}, 400

        data = request.get_json() #add force=True to ignore but risky
                                  #silent=True just returns none instead of error
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201 #status code

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message' : "Item: '{}' deleted".format(name)}, 200

    def put(self, name):
        data = request.get_json()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name':name, 'price':data['price']}
            items.append(item)
        else:
            item.update(data)
        return item



class ItemList(Resource):
    def get(self):
        return {'items': items}


#code below identical to@app.route('student...') decorator
api.add_resource(Item, '/item/<string:name>') #i.e http://...../item/<name>
api.add_resource(ItemList, '/items')
app.run(port=5000, debug=True) #html error page generated


# TEST FIRST DESIGN Approach
# This forces you to identify the need for these request before just jumping into
# creating endpoints
#
# refer to Postman section 4 folder
#
# If you are just dealing with items...what is necessary?
# GET items - this should return the list of items, each in JSON format
# GET item by UID
# POST item to create a new item. duplicate id not allowed
# DELETE item by UID
# PUT item create/update item by UID
