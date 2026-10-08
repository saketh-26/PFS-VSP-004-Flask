from flask import Flask
import uuid
app = Flask(__name__)
#Build a Student routing app
#Student default page #Student id
#student attendance
#file path
#student uuid
#courses 
@app.route('/')
def students():
    return f'Student Routing Application'
@app.route('/studentid/<int:id>')
def stu_id(id):
    return f'The Student ID is{id}'
@app.route('/attendance/<float:st_attendance>')
def stu_att(st_attendance):
    return f'The Student attendance is {st_attendance}'
@app.route('/skills/<s1>/<s2>')
def skills(s1,s2):
    return f'Student has {s1} and {s2} Skills'
@app.route('/details/<path:file_path>')
def details(file_path):
    return f'The path is {file_path}'
@app.route('/search_student/')
def generate():
    id = uuid.uuid4().hex
    return f'The Student search id = {id}'
if __name__ == "__main__":
    app.run(host='0.0.0.0',
            port = 5002,debug=True)