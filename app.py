from flask import Flask, jsonify, request, render_template#for applications

app = Flask(__name__)

#setting the route with a decorator
@app.route('/') #'e.g. http://www.google.com/ <--- homepage of the site'
def home():
   return render_template('index.html')


#HTTP verbs
#POST - used to receive data
#GET - used to send data back only
#PUT - used to ensure data is there
#DELETE - used to delete a resource

#Examples building a store app
stores = [ # list of dict of stores and list of dict of items in each store
    {
        'name': 'My Wonderful Store',
        'items':[
            {
                'name': 'My Item',
                'price': 15.99
            }
        ]

    }
]


#POST /store data: {name:}
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json() #retrieve post data
    new_store = {
        'name':request_data['name'],
        'items':[]
    }
    stores.append(new_store)
    return jsonify(new_store)

#GET /store/<string:name>
@app.route('/store/<string:name>') #http://127.0.01:50000/store.some_name passed as param
def get_store(name):
    #Iterate over stores
    #if the store name matches, return it
    #if none match return an error message
    for store in stores:
        if(store['name'] == name):
            return jsonify(store)
    return jsonify({'message':'store not found'})

#GET /store
@app.route('/store') #methods=['GET'] defaulted
def get_stores():
    return jsonify({'stores': stores})

#POST /store/<string:name>/item {name:, price:}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json() #retrieve post data
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message':'store not found'})

#GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_items_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})
    return jsonify({'message': 'store not found'})

app.run(port = 5000)


#JSON is essentially a dictionary of key value pairs
#used to send inofmraiton from one application to another
#HOWEVER JSON is not of type dict it is of type string. So it is necessary to convert
#Flask has a method called jsonify which can be imported
#JSON cannot be lists so lists must be converted to dicts see get_Stores for example
#JSON rendered always uses double quotes " " as opposed to the single quotes ' ' in the dict
