from config import Config
import mysql.connector as sql
import random
import smtplib
from email.message import EmailMessage
from flask import Flask,render_template,redirect,url_for,request
app = Flask(__name__)
DBConfig = Config()
from_email = DBConfig.from_email
email_app_password = DBConfig.email_app_password
#We will first make connection with DB
def getConnectionWithDB():
    db_host = DBConfig.db_host
    db_port = DBConfig.db_port
    db_user = DBConfig.db_user
    db_password = DBConfig.db_password
    db_name = DBConfig.db_name
    #print(db_name,db_host)
    try:
        connection = sql.connect(
            host=db_host,
            port = db_port,
            user = db_user,
            password = db_password,
            database = db_name
        )
        return connection
    except:
        return "Connection Failed"
#Insert the data into the table
def insertUserRecord(user_data):
    """Inserting User records"""
    name = user_data['name']
    email = user_data['email']
    password_hash = user_data['password_hash']
    connection = getConnectionWithDB()
    if connection == "Connection Failed":
        return False
    else:
        try:
            cursor = connection.cursor()
            cursor.execute(
            "INSERT INTO users(name,email,password_hash) values(%s,%s,%s)",(name,email,password_hash))
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except:
            print("Data cannot be inserted")
            return False
#Now let us  define the data
data = [
    {
        'name': 'Shekar',
        'email': 'shekar1505@gmail.com',
        'password_hash': '1a2b3c4d'
    },
    {
        'name': 'Mamatha',
        'email': 'mamtha0803@gmail.com',
        'password_hash': '5e6f7g8h'
    },
    {
        'name': 'Sai',
        'email': 'Sai@codegnan.com',
        'password_hash': '9i0j1k2l'
    }
]
#for user in data:
# #    result = insertUserRecord(user)

#Let us create multiple functions to access the data from
#the tables,along with specific user wise (id,name,email)

def readUserRecords():
    connection = getConnectionWithDB()
    if connection == "Connection Failed":
        return False
    else:
        cursor = connection.cursor()
        cursor.execute("SELECT * from users")
        data = cursor.fetchall()
        records = []
        for record in data:
            temp = {}
            #print(record)
            temp['id'] = record[0]
            temp['name'] = record[1]
            temp['email'] = record[2]
            temp['password_hash'] = record[3]
            temp['is_verified'] = record[4]
            temp['created_at'] = record[5]
            records.append(temp)
        cursor.close()
        connection.close()
        return records
#print(readUserRecords())
def readUserRecordbyEmail(user_data):
    email = user_data['email']
    connection = getConnectionWithDB()
    if connection == "Connection Failed":
        return False
    else:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * from users where email=%s",
                       (email,))
            data = cursor.fetchone()
        #print(data)
            record = {
                "id":data[0],
                "name":data[1],
                "email":data[2],
                "password_hash":data[3],
                "is_verified":data[4],
                "created_at":data[5]}
            return record
        except:
             cursor.close()
             connection.close()
             return "No Record"
def readUserRecordbyId(user_data):
    id=user_data['id']
    connection=getConnectionWithDB()
    if connection=='Connection Failed':
        return False
    else:
        cursor=connection.cursor()
        cursor.execute("SELECT * from users where id=%s",(id,))
        data=cursor.fetchone()
        try:
            record={
                'id':data[0],
                'name':data[1],
                'email':data[2],
                'password_hash':data[3],
                'is_verified':data[4],
                'created_at':data[5]
            }
            cursor.close()
            connection.close()
            return record
        except:
            cursor.close()
            connection.close()
            return 'No record'

def updateNamebyIDorEmail(user_data):
    query_filter = ""
    try:
        id = user_data['id']
        query_filter = 'id'
    except:
        email = user_data['email']
        query_filter = "email"
    new_name = user_data['new_name']
    connection = getConnectionWithDB()
    if connection == "Connection Failed":
        return False
    else:
        cursor = connection.cursor()
        if query_filter == "id":
            query = "UPDATE users SET name = %s WHERE id = %s"
            values = (new_name,id)
        elif query_filter == "email":
            query = "UPDATE users SET name = %s WHERE email =%s"
            values = (new_name,email)
        cursor.execute(query,values)
        connection.commit()
        cursor.close()
        connection.close()
        return True
def updatePasswordByIdorEmail(user_data):
    query_filter = ""
    try:
        id = user_data['id']
        query_filter='id'
    except:
        email=user_data['email']
        query_filter='email'
    new_password = user_data['new_password']
    connection = getConnectionWithDB()
    if connection == "Connection Failed":
        return False
    else:
        cursor = connection.cursor()
        if query_filter == "id":
            query = "UPDATE users SET password_hash=%s WHERE id=%s"
            values = (new_password,id)
        elif query_filter == "email":
            query = "UPDATE users SET password_hash=%s WHERE email =%s"
            values = (new_password,email)
        cursor.execute(query,values)
        connection.commit()
        cursor.close()
        connection.close()
        return True
def updateVerifiedByIdorEmail(user_data):
    query_filter = ""
    try:
        id = user_data['id']
        query_filter='id'
    except:
        email=user_data['email']
        query_filter='email'
    verified = user_data['verified']
    connection = getConnectionWithDB()
    if connection == "Connection Failed":
        return False
    else:
        cursor = connection.cursor()
        if query_filter == "id":
            query = "UPDATE users SET is_verified=%s WHERE id=%s"
            values = (verified,id)
        elif query_filter == "email":
            query = "UPDATE users SET is_verified=%s WHERE email =%s"
            values = (verified,email)
        cursor.execute(query,values)
        connection.commit()
        cursor.close()
        connection.close()
        return True
def generateOTP():
    otp = random.randint(1000,9999)
    return otp
def sendOTPviaemail(to_email,otp):
    message = EmailMessage()
    message['Subject'] = "OTP Notification"
    message['From'] = from_email
    message['To'] = to_email
    message.set_content(
        f"Your OTP is {otp}"
    )
    with smtplib.SMTP("smtp.gmail.com",587) as server:
        server.starttls()
        server.login(from_email,email_app_password)
        server.send_message(message)
    return True

#sendOTPviaemail('sakethreddy.kallepu@gmail.com',5423)
def validateData(user_data):
    errors =[]
    name=user_data['name']
    email=user_data['email']
    password = user_data['password']
    confirm_password = user_data['confirm_password']
user_data = {'id':2,
             'name':"Shekar",
             'email':'shekar1505@gmail.com',
             'new_password':'admin1234',
             'verified':True}
#print(updateNamebyIDorEmail(user_data))
#print(updateVerifiedByIdorEmail(user_data))
#print(generateOTP())
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if (request.method =="GET"):
        return render_template('register.html')
    elif (request.method=="POST"):
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password  = request.form['confirm_password']
        user_data = {
            "name":name,
            "email":email,
            "password":password,
            "confirm_password":confirm_password
        }
        errors = validateData(user_data)
        return render_template('register.html',
                               errors=errors)
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
if (__name__ == "__main__"):
    app.run(host="0.0.0.0",
            port = 5003,
            debug=True)