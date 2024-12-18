# Import necessary libraries
from flask import Flask, abort, jsonify  # Import Flask framework and helper functions
from flask_restx import Api, Resource, fields  # Import Flask-RESTx for building REST APIs

# Create a Flask application instance
app = Flask(__name__)

# Create an API instance using the Flask app
my_api = Api(app, version='1.0', title='Sample API',
              description='A simple demonstration of a Flask RESTX API')

# Define a model for user input using Flask-RESTx fields
user_model = my_api.model('User', {
    'id': fields.Integer(required=True, description='The user ID'),  # User ID field
    'name': fields.String(required=True, description='The user name')  # User name field
})

# In-memory storage for users, simulating a database
users = [
    {'id': 1, 'name': "one"},   # Sample user 1
    {'id': 2, 'name': "two"},   # Sample user 2
    {'id': 3, 'name': "three"}   # Sample user 3
]

# Define the UserList resource for handling user collection endpoints
@my_api.route('/users')
class UserList(Resource):
    """Shows a list of all users and allows adding new users"""

    def get(self):
        """List all users"""
        return jsonify(users)  # Return the list of users as JSON

    @my_api.expect(user_model)  # Specify the expected model for POST requests
    def post(self):
        """Create a new user"""
        new_user = my_api.payload  # Get the payload (data) from the request
        # Check for missing fields in the incoming data
        if 'id' not in new_user or 'name' not in new_user:
            # Return an error message and status code 400 for bad request
            return {'message': f"Missing id or name in the request body"}, 400
        
        users.append(new_user)  # Add the new user to the in-memory storage
        # Return the created user's ID and name with status code 201 for created
        return {'id': new_user['id'], 'name': new_user['name']}, 201

# Define the UserResource for handling specific user operations
@my_api.route('/users/<int:user_id>')  # Define a route with a variable user_id
class UserResource(Resource):
    
    def get(self, user_id):
        """Get a user by ID"""
        # Find the user in the list by ID
        user = next((user for user in users if user['id'] == user_id), None)
        # Check if user is found; if not, return an error message
        if user is None:
            return {'message': f"User with ID {user_id} has not found"}, 400
        return user  # Return the found user

    @my_api.expect(user_model)  # Specify the expected model for PUT requests
    def put(self, user_id):
        """Update a user by ID"""
        # Find the user in the list by ID
        user_to_update = next((user for user in users if user['id'] == user_id), None)
        # Check if user is found; if not, return an error message
        if user_to_update is None:
            return {'message': f"User with ID {user_id} has not found"}, 400
        
        updated_user = my_api.payload  # Get the updated data from the request
        user_to_update['name'] = updated_user['name']  # Update the user's name
        # Return a success message with status code 200 for success
        return {'message': f"User with ID {user_id} updated"}, 200

    def delete(self, user_id):
        """Delete a user by ID"""
        # Find the user in the list by ID
        user_to_delete = next((user for user in users if user['id'] == user_id), None)
        # Check if user is found; if not, return an error message
        if user_to_delete is None:
            return {'message': f"User with ID {user_id} has not found"}, 400
        
        users.remove(user_to_delete)  # Remove the user from the in-memory storage
        # Return a success message with status code 200 for success
        return {'message': f"User with ID {user_id} has been deleted"}, 200

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0')  # Start the Flask application, accessible from any host
