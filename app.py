import json
from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"

CORS(app)
db = SQLAlchemy(app)

# Model
class Students(db.Model):
    id = db.Column('student_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))
    pin = db.Column(db.String(10))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'car': self.city,
            'year': self.addr,
            'fix': self.pin
        }

@app.route("/")
def hello_world():
    students_list = [student.to_dict() for student in Students.query.all()]
    json_data = json.dumps(students_list)
    return json_data

@app.route("/del/<int:id>", methods=['DELETE'])
def del_student(id):
    student = Students.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return {"delete": "success"}

@app.route("/upd/<int:id>", methods=['PUT'])
def upd_student(id):
    student = Students.query.get_or_404(id)
    data = request.get_json()
    student.name = data['clientname']
    student.city = data['car']
    student.addr = data['year']
    student.pin = data['fix']
    db.session.commit()
    return {"update": "success"}

@app.route('/new', methods=['POST'])
def new():
    data = request.get_json()
    name = data['clientname']
    city = data['car']
    addr = data['year']
    pin = data['fix']

    new_student = Students(name=name, city=city, addr=addr, pin=pin)
    db.session.add(new_student)
    db.session.commit()
    return "A new record was created."

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
