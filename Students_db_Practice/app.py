from flask import Flask,render_template,request,redirect,url_for,jsonify
import db_utils

app=Flask( __name__)

@app.route('/')
def home():
    return "<h1>Welcome to Students Database Management System</h1>"

@app.route('/students',methods=['GET'])
def get_students():
    students=db_utils.fetch_students()
    return jsonify(students)

@app.route('/students',methods=['POST'])
def add_student():
    data=request.get_json()
    name=data.get('name')
    subject=data.get('subject') 
    roll_no=data.get('roll_no')
    marks=data.get('marks')
    db_utils.insert_student(name,subject,roll_no,marks)
    return jsonify({'message':'Student added successfully'})    

@app.route('/students/<int:id>',methods=['PUT'])
def update_student(id):
    data=request.get_json()
    name=data.get('name')
    subject=data.get('subject')
    roll_no=data.get('roll_no')
    marks=data.get('marks')
    db_utils.update_student(id,name,subject,roll_no,marks)
    return jsonify({'message':'Student updated successfully'})

@app.route('/students/<int:id>',methods=['GET'])
def get_student(id):
    students=db_utils.fetch_students()
    student=next((student for student in students if student[0]==id),None)
    if student is None:
        return jsonify({'error':'Student not found'})
    return jsonify(student)

@app.route('/students/<int:id>',methods=['DELETE'])
def delete_student(id):
    db_utils.delete_student(id)
    return jsonify({'message':'Student deleted successfully'})

@app.route('/students/average/<subject>',methods=['GET'])
def get_average_marks(subject):
    average_marks=db_utils.find_average_marks(subject)
    if average_marks is None:
        return jsonify({'error':'Subject not found'})
    return jsonify({'average_marks':average_marks})

@app.route('/students/topper',methods=['GET'])
def get_topper():
    topper=db_utils.find_topper()
    if topper is None:
        return jsonify({'error':'No students found'})
    return jsonify({'topper':topper})

if __name__=='__main__':  
    app.run(debug=True)
    db_utils.create_table()  # Ensure the table is created before running the app




