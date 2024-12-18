from datetime import datetime
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource, fields

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://senscio:Agile2022%23@192.168.2.12/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Employee model
class Emp_Api(db.Model):
    e_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    position = db.Column(db.String, nullable=False)
    dept = db.Column(db.String, nullable=True)
    date_hire = db.Column(db.Date, nullable=True)
    email = db.Column(db.String, nullable=False)
    pno = db.Column(db.String, nullable=False)
    salary = db.Column(db.Float, nullable=False)

    def serializer(self):
        return {
            'id': self.e_id,
            'name': self.name,
            'position': self.position,
            'dept': self.dept if self.dept else None,
            'date_hire': self.date_hire.isoformat() if self.date_hire else None,
            'email': self.email,
            'pno': self.pno,
            'salary': self.salary
        }

# Department model
class Dept_Api(db.Model):
    d_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def serializer(self):
        return {
            'id': self.d_id,
            'name': self.name
        }

# Create all tables
with app.app_context():
    db.create_all()

# Create API instance
api = Api(app, version='1.0', title='Employee Management API',
          description='A simple API for managing employees and departments')

# Define namespaces
"""
api.namespace(): This method creates a new namespace. It takes two primary arguments:
'departments': The name of the namespace, which will be part of the URL for the endpoints (e.g., /departments/).
description='Department operations': A brief description of what this namespace handles. This is displayed in the Swagger UI.
"""
employee_ns = api.namespace('employees', description='Employee operations')
department_ns = api.namespace('departments', description='Department operations')

# Employee model for API
employee_model = employee_ns.model('Employee', {
    'e_id': fields.Integer(required=True, description='Employee ID'),
    'name': fields.String(required=True, description='Employee Name'),
    'position': fields.String(required=True, description='Employee Position'),
    'dept': fields.String(description='Employee Department'),
    'date_hire': fields.Date(description='Employee Hire Date'),
    'email': fields.String(required=True, description='Employee Email'),
    'pno': fields.String(required=True, description='Employee Phone Number'),
    'salary': fields.Float(required=True, description='Employee Salary')
})

# Department model for API
department_model = department_ns.model('Department', {
    'd_id': fields.Integer(required=True, description='Department ID'),
    'name': fields.String(required=True, description='Department Name'),
})

# Employee resource
@employee_ns.route('/')
class EmpList(Resource):
    def get(self):
        """Get list of employees"""
        emps = Emp_Api.query.all()
        return jsonify([emp.serializer() for emp in emps])

    @employee_ns.expect(employee_model)
    def post(self):
        """Add a new employee"""
        new_emp = api.payload
        emp = Emp_Api(
            name=new_emp['name'],
            position=new_emp['position'],
            dept=new_emp.get('dept'),
            date_hire=datetime.strptime(new_emp['date_hire'], '%Y-%m-%d').date() if 'date_hire' in new_emp else None,
            email=new_emp['email'],
            pno=new_emp['pno'],
            salary=new_emp['salary']
        )
        db.session.add(emp)
        db.session.commit()
        return jsonify(emp.serializer())

@employee_ns.route('/<int:emp_id>')
class EmpResources(Resource):
    def get(self, emp_id):
        """Get an employee by ID"""
        emp = Emp_Api.query.get(emp_id)
        if emp:
            return jsonify(emp.serializer())
        return {'message': f"Employee with ID {emp_id} not found."}, 404

    @employee_ns.expect(employee_model)
    def put(self, emp_id):
        """Update an employee by ID"""
        emp = Emp_Api.query.get(emp_id)
        if emp:
            new_emp = api.payload
            emp.name = new_emp['name']
            emp.position = new_emp['position']
            emp.dept = new_emp.get('dept')
            emp.date_hire = datetime.strptime(new_emp['date_hire'], '%Y-%m-%d').date() if 'date_hire' in new_emp else None
            emp.email = new_emp['email']
            emp.pno = new_emp['pno']
            emp.salary = new_emp['salary']
            db.session.commit()
            return {'message': f"Employee with ID {emp_id} updated successfully."}
        return {'message': f"Employee with ID {emp_id} not found."}, 404

    def delete(self, emp_id):
        """Delete an employee by ID"""
        emp = Emp_Api.query.get(emp_id)
        if emp:
            db.session.delete(emp)
            db.session.commit()
            return {'message': f"Employee with ID {emp_id} deleted successfully."}
        return {'message': f"Employee with ID {emp_id} not found."}, 404

# Department resource
@department_ns.route('/')
class DeptList(Resource):
    def get(self):
        """Get list of departments"""
        depts = Dept_Api.query.all()
        return jsonify([dept.serializer() for dept in depts])

    @department_ns.expect(department_model)
    def post(self):
        """Add a new department"""
        new_dept = api.payload
        dept = Dept_Api(name=new_dept['name'])
        db.session.add(dept)
        db.session.commit()
        return jsonify(dept.serializer()), 201

@department_ns.route('/<int:d_id>')
class DeptResources(Resource):
    def get(self, d_id):
        """Get a department by ID"""
        dept = Dept_Api.query.get(d_id)
        if dept:
            return jsonify(dept.serializer())
        return {'message': f"Department with ID {d_id} not found."}, 404

    @department_ns.expect(department_model)
    def put(self, d_id):
        """Update a department by ID"""
        dept = Dept_Api.query.get(d_id)
        if dept:
            new_dept = api.payload
            dept.name = new_dept['name']
            db.session.commit()
            return {'message': f"Department with ID {d_id} updated successfully."}
        return {'message': f"Department with ID {d_id} not found."}, 404

    def delete(self, d_id):
        """Delete a department by ID"""
        dept = Dept_Api.query.get(d_id)
        if dept:
            db.session.delete(dept)
            db.session.commit()
            return {'message': f"Department with ID {d_id} deleted successfully."}
        return {'message': f"Department with ID {d_id} not found."}, 404

if __name__ == '__main__':
    app.run(host='0.0.0.0')
