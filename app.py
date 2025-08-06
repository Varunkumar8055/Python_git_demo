from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# In-memory database
items = [
    {'id': 1, 'name': 'Laptop', 'price': 234433},
    {'id': 2, 'name': 'hp', 'price': 5000}
]

@app.route("/")
def home():
    return jsonify({'message': 'Welcome to Flask REST API.'})

# Get all items
@app.route("/items", methods=['GET'])
def get_items():
    return jsonify(items)

# Get single item by ID
@app.route('/items/<int:itemid>', methods=['GET'])
def get_item(itemid):
    item = next((i for i in items if i['id'] == itemid), None)
    if item:
        return jsonify(item)
    abort(404, description='Item not found.')

# Create a new item
@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()

    # Validate input
    if not data or 'name' not in data or 'price' not in data:
        abort(400, description='Invalid input. Must include "name" and "price".')

    try:
        price = float(data['price'])
    except (ValueError, TypeError):
        abort(400, description='Price must be a number.')

    newid = items[-1]['id'] + 1 if items else 1
    item = {
        "id": newid,
        "name": data['name'],
        "price": price
    }

    items.append(item)
    return jsonify(item), 201

# Update an existing item
@app.route('/items/<int:itemid>', methods=['PUT'])
def update_item(itemid):
    item = next((i for i in items if i['id'] == itemid), None)
    if item is None:
        abort(404, description="Item not found.")
    if not request.json:
        abort(400, description="No data provided.")

    name = request.json.get('name', item['name'])

    try:
        price = float(request.json.get('price', item['price']))
    except (ValueError, TypeError):
        abort(400, description="Price must be a number.")

    item['name'] = name
    item['price'] = price

    return jsonify(item)

# Delete an item
@app.route('/items/<int:itemid>', methods=['DELETE'])
def delete_item(itemid):
    global items
    items = [i for i in items if i['id'] != itemid]
    return jsonify({'message': 'Item deleted'})

if __name__ == '__main__':
    app.run(debug=True)
