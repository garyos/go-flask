from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)

api = Api(app)

items = []


class Item(Resource):
    def get(self, name):    #defines the get http method
        for item in items:
            if item['name'] == name:
                return item #FLASK-RESTFUL does not require jsonify
        return {'item': None}, 404 #status code - note return must be in JSON

    def post(self, name):
        data = request.get_json() #add force=True to ignore but risky
                                  #silent=True just returns none instead of error
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201 #status code

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
