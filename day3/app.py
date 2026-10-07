from flask import Flask
app = Flask(__name__)
#Multiple routes to one view function
@app.route('/')
@app.route('/home/')
def home():
    return f'Welcome to Day-3 Learning about Static vs Dynamic routes'
@app.route('/profile/')
def details():
    return f'Hello this is Saketh'
#static routing --> /name/saketh
#dynamic routing -->/name/<name>
@app.route('/name/saketh') #static route
def data():
    return f'Welcome Saketh...'
@app.route('/name/<name>') #dynamic route check the names 
def student_name(name):
    return f'Hello {name}'
#Now we want to create related to course names
@app.route('/courses/<course_name>')
def courses(course_name):
    return f'<b> This Course is:{course_name} </b>'
#converters --> int,str,float,path,uuid
#Integer converters
@app.route('/students/<int:student_id>')
def studentid(student_id):
    return f'The ID of Student is {student_id}'
#Float converters
@app.route('/percentages/<float:percentage>')
def stupercentages(percentage):
    return f'The Percentage of Student is {percentage}'
#Path converters
@app.route('/path/<path:file_name>')
def filepath(file_name):
    return f'The path is {file_name}'
#UUID -->Universal Unique Identifier
@app.route('/student_id/<uuid:stu_id>')
def student_id(stu_id):
    return f'The Search for Student is {stu_id}'
if __name__ == "__main__":
    app.run(host='0.0.0.0',
            port=5001,debug=True)
