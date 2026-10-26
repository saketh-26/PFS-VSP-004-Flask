from config import Config
import mysql.connector as sql
DBConfig = Config()
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

    
user_data = {"id":45}
print(readUserRecordbyEmail(user_data))

