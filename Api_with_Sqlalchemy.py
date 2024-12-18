from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable track modifications
db = SQLAlchemy(app)  # Create a SQLAlchemy instance

# Define the Item model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key column
    name = db.Column(db.String(100), nullable=False)  # Name column

    def __repr__(self):
        return f"Item('{self.id}', '{self.name}')"

# Create the database and tables
with app.app_context():
    db.create_all()
    
# """
# Creating an Application Context: When you run the code inside the with app.app_context(): block:
# Flask temporarily makes the app instance available for use within that block.
# This allows you to access the app’s configuration, database connection, and other context-specific features.
# """

# GET all items
@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()  # Query all items from the database
    return jsonify([{'id': item.id, 'name': item.name} for item in items])  # Convert to JSON

# GET a specific item
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Item.query.get(item_id)  # Get item by ID
    if item is None:
        return jsonify({'message': 'Item not found'}), 404  # Not found response
    return jsonify({'id': item.id, 'name': item.name})  # Return item data

# POST a new item
@app.route('/items', methods=['POST'])
def add_item():
    new_item = request.json  # Get JSON data from the request
    item = Item(name=new_item['name'])  # Create a new Item instance
    db.session.add(item)  # Add to session
    db.session.commit()  # Commit to the database
    return jsonify({'id': item.id, 'name': item.name}), 201  # Return created item

# PUT to update an item
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = Item.query.get(item_id)  # Get item by ID
    if item is None:
        return jsonify({'message': 'Item not found'}), 404  # Not found response
    updated_data = request.json  # Get updated data from the request
    item.name = updated_data['name']  # Update the item's name
    db.session.commit()  # Commit the changes
    return jsonify({'id': item.id, 'name': item.name})  # Return updated item

# DELETE an item
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get(item_id)  # Get item by ID
    if item is None:
        return jsonify({'message': 'Item not found'}), 404  # Not found response
    db.session.delete(item)  # Delete the item
    db.session.commit()  # Commit the changes
    return jsonify({'message': 'Item deleted'}), 204  # Return no content response

if __name__ == "__main__":
    app.run(host='0.0.0.0')
