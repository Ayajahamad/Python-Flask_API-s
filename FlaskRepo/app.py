from flask import Flask, jsonify, request

# Flask: The main class for creating the Flask application.
# jsonify: A helper function to convert Python dictionaries into JSON responses.
# request: An object that contains all the information about the incoming request, including the request data.

app = Flask(__name__)
# Initializes a new Flask application instance. The __name__ argument helps Flask understand where to look 
    # for resources and templates.

# Sample data: a list of items
items = [
    {'id': 1, 'name': 'Item 1'},
    {'id': 2, 'name': 'Item 2'},
]

print(items)

# GET all items
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)

    # Endpoint: /items with the GET method.
    # Function: When a GET request is made to this endpoint, it returns all items in JSON format.
    # Response: The jsonify function converts the items list into a JSON response.

# GET a specific item
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    if item is None:
        return jsonify({'message': 'Item not found'}), 404
    return jsonify(item)

# POST a new item
@app.route('/items', methods=['POST'])
def add_item():
    new_item = request.json
    new_item['id'] = len(items) + 1
    items.append(new_item)
    return jsonify(new_item), 201

    # Endpoint: /items with the POST method.
    # Function: Adds a new item to the list.
    # Retrieves the new item data from the request body using request.json.
    # Assigns a unique ID to the new item.
    # Appends the new item to the items list.
    # Response: Returns the newly created item with a status code of 201 (Created).

# PUT to update an item
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    if item is None:
        return jsonify({'message': 'Item not found'}), 404

    updated_data = request.json
    item.update(updated_data)
    return jsonify(item)

# DELETE an item
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global items
    items = [item for item in items if item['id'] != item_id]
    return jsonify({'message': 'Item deleted'}), 204

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host='0.0.0.0')
    




# Creating an Application Context: When you run the code inside the with app.app_context(): block:

# Flask temporarily makes the app instance available for use within that block.
# This allows you to access the app’s configuration, database connection, and other context-specific features.