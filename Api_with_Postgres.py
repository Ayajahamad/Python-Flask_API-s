import psycopg2

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

"""
Database Configuration:
Update the database URI (postgresql://username:password/database) with your 
PostgreSQL username, password, and database name.
"""

# Database configuration
# Localhost: If the PostgreSQL server is running on the same machine as your Flask application, you can use localhost or 127.0.0.1. For example:
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://senscio:Agile2022%23@localhost/test'

# Remote Server: If the PostgreSQL database is hosted on a different server, you need to replace server_ip_address with the actual IP address or hostname of that server. For example:
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://senscio:Agile2022%23@192.168.2.12/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

"""
By setting app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] to False, 
you're opting out of this modification tracking, which can help improve the performance of your application, 
especially in larger applications with many database interactions.
"""


db = SQLAlchemy(app)

"""
db: In a Flask application using Flask-SQLAlchemy, db is typically an instance of the SQLAlchemy class. This instance is responsible for handling the database connection, as well as providing the tools for working with the ORM.

Model: Model is a class provided by Flask-SQLAlchemy that represents a base class for all your database models. When you define a class that inherits from db.Model, you are telling Flask-SQLAlchemy that this class is a database model that should be mapped to a table in your database.
Defining Your Data Structure:

By inheriting from db.Model, your Item class can define attributes that represent columns in the corresponding database table. SQLAlchemy will manage the relationship between the attributes of your model and the columns of the database table.
"""
# Define a simple Item model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }

# Create the database and tables
with app.app_context():
    db.create_all()
"""
Creating an Application Context: When you run the code inside the with app.app_context(): block:
Flask temporarily makes the app instance available for use within that block.
This allows you to access the app's configuration, database connection, and other context-specific features.
"""

# Home Page
@app.route('/')
def Home():
    return "Home Page"


# GET all items
@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    print(items)
    return jsonify([item.serialize() for item in items])

# GET a specific item
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Item.query.get(item_id)
    if item is None:
        return jsonify({'message': 'Item not found'}), 404
    return jsonify(item.serialize())

# POST a new item
@app.route('/items', methods=['POST'])
def add_item():
    new_item_data = request.json
    new_item = Item(name=new_item_data['name'])
    db.session.add(new_item)
    db.session.commit()
    return jsonify(new_item.serialize()), 201

# PUT to update an item
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = Item.query.get(item_id)
    if item is None:
        return jsonify({'message': 'Item not found'}), 404

    updated_data = request.json
    item.name = updated_data.get('name', item.name)
    db.session.commit()
    return jsonify(item.serialize())

# DELETE an item
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get(item_id)
    if item is None:
        return jsonify({'message': 'Item not found'}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted'}), 204

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host='0.0.0.0')
