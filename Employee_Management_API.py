from datetime import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource, fields
from sqlalchemy import delete  # Import Flask-RESTx for building REST APIs

"""
Flask(__name__): Initializes a Flask application. __name__ refers to the current module, which helps Flask 
determine the root path for the application.
"""
app = Flask(__name__)

"""
SQLALCHEMY_DATABASE_URI: This configuration variable specifies the database connection string. In your case, 
it's for a PostgreSQL database.
SQLALCHEMY_TRACK_MODIFICATIONS: When set to False, this disables the modification tracking system, which is 
not needed for most applications and can save memory.
"""
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://senscio:Agile2022%23@192.168.2.12/test'  # Database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable track modifications

"""
db = SQLAlchemy(app):
This creates an instance of the SQLAlchemy class, passing the Flask app to it. This instance will be used to 
interact with the database.
"""
db = SQLAlchemy(app)

"""
class Emp_ApiD(db.Model): This defines a new model class that corresponds to a table in the database.

db.Column: Defines a column in the table. Parameters include:

Type: Such as db.Integer, db.String, db.Float, etc.
primary_key=True: Indicates that this column is the primary key.
nullable=False: Specifies whether the column can accept null values.
Each attribute in the class corresponds to a column in the database table.
"""

class Emp_ApiD(db.Model):
    e_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    position = db.Column(db.String, nullable=False)
    dept = db.Column(db.String, nullable=True)
    date_hire = db.Column(db.Date, nullable=True)
    email = db.Column(db.String, nullable=False)
    pno = db.Column(db.String, nullable=False)
    salary = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f"<User id={self.e_id}, name='{self.name}' , position={self.position}, dept={self.dept}, hire_date={self.date_hire}, email={self.email} , pno={self.email}, salary={self.salary}>" 

    def serializer(self):
        return  {
                'id' : self.e_id,
                'name' : self.name,
                'position' : self.position, 
                'dept' : self.dept if self.dept else None, 
                'date_hire': self.date_hire.isoformat() if self.date_hire else None, 
                'email' : self.email, 
                'pno' : self.pno, 
                'salary' : self.salary
               }

"""
with app.app_context(): This creates a context for the application, allowing you to work with the database 
within this block.
db.create_all(): Creates all the tables defined in the models in the database. This is usually done once to 
set up the database schema.
"""

with app.app_context():
    db.create_all()
    
"""
Api(app, ...): Initializes a Flask-RESTx API instance with the Flask app. It includes options for versioning, 
titles, and descriptions for API documentation.
"""
# Create an API instance using the Flask app
my_api = Api(app, version='1.0', title='API to Manage Employees',
              description='A simple demonstration of Flask API with Employee Management Project..!')


"""
my_api.model('User', {...}): Defines a data model for the API. This model describes the structure of the 
expected input/output for the API.
fields: Defines the type of each field in the model, along with metadata such as whether it's required and a 
description.
"""
# Define a model for user input using Flask-RESTx fields
user_model = my_api.model('User', {
    'e_id': fields.Integer(required=True, description='The Employee ID'),  # User ID field
    'name': fields.String(required=True, description='The Employee Name'),  # User name field
    'position': fields.String(required=True, description='The Employee Position'),
    'dept': fields.String(required=True, description='The Employee Department'),
    'date_hire': fields.Date(required=True, description='The Employee Hire_date'),
    'email': fields.String(required=True, description='The Employee Email'),
    'pno': fields.String(required=True, description='The Employee Phone number'),
    'salary': fields.Float(required=True, description='The Employee Salary')
})

"""
What is Resource?
Definition:
Resource is a class that represents a single resource in a RESTful API. In REST, a resource is any entity that 
can be represented and interacted with, such as users, products, or orders.

Usage:
When you create a class that inherits from Resource, you can define methods that correspond to the different 
HTTP methods (like GET, POST, PUT, DELETE) that can be performed on that resource.
"""

@my_api.route('/employees')
class EmpList(Resource):
    """Show the list of all Employees and Allows Adding new Emp"""
    
    def get(self):
        """Show the list of all Employees"""
        emps = Emp_ApiD.query.all()
        print(emps)  # Log the employees retrieved for debugging
        return jsonify([emp.serializer() for emp in emps])  # Return only the serialized data
    
    @my_api.expect(user_model)
    def post(self):
        """Add a new Employee"""
        new_emp = my_api.payload
        
        existing_emp = Emp_ApiD.query.get(new_emp['e_id'])
        
        if existing_emp:
            return {'message': f"User with ID {new_emp['e_id']} already exists."}, 400
        
        emp = Emp_ApiD(
            name=new_emp['name'],
            position=new_emp['position'],
            dept=new_emp.get('dept'),  # Use get to avoid KeyError
            date_hire=datetime.strptime(new_emp['date_hire'], '%Y-%m-%d').date() if 'date_hire' in new_emp else None,
            email=new_emp['email'],
            pno=new_emp['pno'],
            salary=new_emp['salary']
        )
        
        db.session.add(emp)
        db.session.commit()
        
        return jsonify(emp.serializer())

@my_api.route('/employees/<int:emp_id>')
class EmpResources(Resource):
    def get(self,emp_id):
        """Get single employee By ID"""
        emp = Emp_ApiD.query.get(emp_id)
        
        if emp:
            print(emp)
            return jsonify(emp.serializer())
        return {'message': f"Employee with ID {emp_id} not present."}, 400
        
    @my_api.expect(user_model)
    def put(self,emp_id):
        """Update a Employee by ID"""
        emp_to_update = Emp_ApiD.query.get(emp_id)
        new_emp = my_api.payload
        if emp_to_update:
            print(emp_to_update)
            
            emp_to_update.name=new_emp['name'],
            emp_to_update.position=new_emp['position'],
            emp_to_update.dept=new_emp.get('dept'),  # Use get to avoid KeyError
            emp_to_update.date_hire=datetime.strptime(new_emp['date_hire'], '%Y-%m-%d').date() if 'date_hire' in new_emp else None,
            emp_to_update.email=new_emp['email'],
            emp_to_update.pno=new_emp['pno'],
            emp_to_update.salary=new_emp['salary']
            
            db.session.commit()

            return {'message': f"Employee with ID {emp_id} Updated Successfully."}
        return {'message': f"Employee with ID {emp_id} not present."}, 400

    def delete(self,emp_id):
        """Delete a Employee by ID"""
        emp_to_delete = Emp_ApiD.query.get(emp_id)
        if emp_to_delete:
            print(emp_to_delete)
            db.session.delete(emp_to_delete)
            db.session.commit()
            return {'message': f"Employee with ID {emp_id} Deleted Successfully."}
        return {'message': f"Employee with ID {emp_id} not present."}, 400

if __name__=='__main__':
    app.run(host='0.0.0.0')