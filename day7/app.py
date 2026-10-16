from flask import Flask,render_template 
app = Flask(__name__)
@app.route('/')
def index():
    data = 18
    #create student details
    student_details = [
        {"id":1,"name":"Saketh"},
         {"id":2,"name":"Saikiran"}
    ]
    return render_template('index.html',d = data,
                           p=student_details)
@app.route('/about/')
def about():
    return render_template('about.html')
if (__name__ == "__main__"):
    app.run(host = "0.0.0.0",
            port = 5002,debug=True)