from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import uuid


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)


# Модель данных для сотрудника
class Employee(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    last_name = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    middle_name = db.Column(db.String(50))
    position = db.Column(db.String(50))

    def __init__(self, last_name, first_name, middle_name, position):
        self.id = str(uuid.uuid4())
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.position = position


# Схема сериализации/десериализации для сотрудника
class EmployeeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'last_name', 'first_name', 'middle_name', 'position')


employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)


# Создание нового сотрудника
@app.route('/employees', methods=['POST'])
def create_employee():
    last_name = request.json['last_name']
    first_name = request.json['first_name']
    middle_name = request.json['middle_name']
    position = request.json['position']

    with app.app_context():
        new_employee = Employee(last_name, first_name, middle_name, position)
        db.session.add(new_employee)
        db.session.commit()

    return employee_schema.jsonify(new_employee)


# Получение всех сотрудников
@app.route('/employees', methods=['GET'])
def get_employees():
    with app.app_context():
        all_employees = Employee.query.all()
        result = employees_schema.dump(all_employees)
        return jsonify(result)


# Получение информации о конкретном сотруднике по его идентификатору
@app.route('/employees/<id>', methods=['GET'])
def get_employee(id):
    with app.app_context():
        employee = Employee.query.get(id)
        return employee_schema.jsonify(employee)


# Обновление информации о сотруднике
@app.route('/employees/<id>', methods=['PUT'])
def update_employee(id):
    with app.app_context():
        employee = Employee.query.get(id)

        last_name = request.json['last_name']
        first_name = request.json['first_name']
        middle_name = request.json['middle_name']
        position = request.json['position']

        employee.last_name = last_name
        employee.first_name = first_name
        employee.middle_name = middle_name
        employee.position = position

        db.session.commit()

    return employee_schema.jsonify(employee)


# Удаление сотрудника
@app.route('/employees/<id>', methods=['DELETE'])
def delete_employee(id):
    with app.app_context():
        employee = Employee.query.get(id)
        db.session.delete(employee)
        db.session.commit()
        return employee_schema.jsonify(employee)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()