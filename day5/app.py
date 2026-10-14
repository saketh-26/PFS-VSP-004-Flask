from flask import Flask,redirect,render_template,url_for,request
#create a flask application instance
app = Flask(__name__)
@app.route('/')
def home():
    #return f'Flask Server is running'
    return render_template('index.html')
#name = saketh,email = saketh@codegnan.com
#GET --> fetching the data from db
#POST --> store the data in db,forms 
#PUT --> update the data (entire row) 
#DELETE --> delete the data (entire row)
#PATCH --> update a specific column in a row 
@app.route('/getData',methods=['GET'])
def getData():
    name = request.args.get('name')
    email = request.args.get('email')
    return f'The name is {name} and email is {email}'
@app.route('/getDatafromPOST',methods = ['POST'])
def getDatafromPOST():
    data = request.get_json()
    name = data['name']
    email = data['email']
    return f'The name is {name},email is {email}'
@app.route('/postData',methods=['POST'])
def postData():
    name = request.form['name']
    email = request.form['email']
    password= request.form['password']
    if name is None or len(name) < 5:
        return render_template('index.html',
                               err="Invalid name")
    if email is None:
        return render_template('index.html',
                               err="Invalid email")
    if password is None or len(password) < 4:
        return render_template('index.html',
                               err="Password is wrong")
    return render_template('index.html',
                           msg = "Successful")
@app.route('/updateData/<email>',methods=['PUT'])
def updateData(email):
    data = request.get_json()
    email1 = data['email']
    print(email1)
    #DATABASE LOGIC for PUT
    return f"Data is updated Successfully for {email}"
@app.route('/deleteData/<email>',methods=['DELETE'])
def deleteData(email):
    #DATABASE Logic for Delete
    return f"Data is deleted successfully for {email}"
if __name__ == "__main__":
    app.run(host='0.0.0.0',
            port = 5002,debug=True)