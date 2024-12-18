from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource, fields # Import Flask-RESTx for building REST APIs

# Initialize Flask app
app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://senscio:Agile2022%23@192.168.2.12/test'  # Database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable track modifications

db = SQLAlchemy(app)  # Create a SQLAlchemy instance

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<User id={self.id}, name='{self.name}'>" 
    
# Create the database and tables
with app.app_context():
    db.create_all()
    
# Create an API instance using the Flask app
my_api = Api(app, version='1.0', title='Sample API',
              description='A simple demonstration of a Flask RESTX API')

# Define a model for user input using Flask-RESTx fields
user_model = my_api.model('User', {
    'id': fields.Integer(required=True, description='The user ID'),  # User ID field
    'name': fields.String(required=True, description='The user name')  # User name field
})

# Define the UserList resource for handling user collection endpoints
@my_api.route('/users')
class UserList(Resource):
    """Shows a list of all users and allows adding new users"""
    
    def get(self):
        """List all users"""
        users = User.query.all()  # Query all users from the database
        return jsonify([{'id': user.id, 'name': user.name} for user in users])  # Return as JSON
    
    @my_api.expect(user_model)  # Specify the expected model for POST requests
    def post(self):
        """Create a new user"""
        new_user = my_api.payload  # Get the payload (data) from the request
        existing_user = User.query.get(new_user["id"])
        
        if existing_user:
             return {'message': f"User with ID {new_user['id']} already exists."}, 400  # Return error if user exists

        user = User(id=new_user['id'], name=new_user['name'])  # Create a User object
        db.session.add(user)  # Add the user to the session
        db.session.commit()  # Commit the session to save the user to the database
        return {'id': user.id, 'name': user.name}, 201  # Return created user
        

# Define the UserResource for handling specific user operations
@my_api.route('/users/<int:user_id>')  # Define a route with a variable user_id
class UserResource(Resource):
    def get(self, user_id):
        """Get a user by ID"""
        # Find the user in the list by ID
        users = User.query.all()
        user = next((user for user in users if user.id == user_id), None)
        # Check if user is found; if not, return an error message
        if user is None:
            return {'message': f"User with ID {user_id} has not found"}, 400
        return {'id':user.id, 'name':user.name},201  # Return the found user
    
    @my_api.expect(user_model)  # Specify the expected model for PUT requests
    def put(self, user_id):
        """Update a user by ID"""
        users = User.query.all()
        # Find the user in the list by ID
        user_to_update = next((user for user in users if user.id == user_id), None)
        print(user_to_update)
        # Check if user is found; if not, return an error message
        if user_to_update is None:
            return {'message': f"User with ID {user_id} has not found"}, 400
        
        updated_user = my_api.payload  # Get the updated data from the request
        user_to_update.name = updated_user['name']  # Update the user's name
        db.session.commit()
        # Return a success message with status code 200 for success
        return {'message': f"User with ID {user_id} updated"}, 200

    def delete(self, user_id):
        """Delete a user by ID"""
        users = User.query.all()
        # Find the user in the list by ID
        user_to_delete = next((user for user in users if user.id == user_id), None)
        print(user_to_delete)
        # Check if user is found; if not, return an error message
        if user_to_delete is None:
            return {'message': f"User with ID {user_id} has not found"}, 400
        
        db.session.delete(user_to_delete)
        db.session.commit()
        # Return a success message with status code 200 for success
        return {'message': f"User with ID {user_id} Deleted"}, 200


if __name__ == "__main__":
    app.run(host='0.0.0.0')
    
