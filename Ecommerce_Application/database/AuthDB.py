from database.connection import DatabaseConnection

#check user exists or not
def getUserByEmail(email:str,data:bool=False):
    try:
        db_config=DatabaseConnection()
        cursor = db_config.cursor(dictionary=True)
        get_user_by_email = """select * from users where
        email = %s;"""
        cursor.execute(get_user_by_email,(email,))
        user = cursor.fetchone()
        cursor.close()
        db_config.close()
        if user:
            if data==True:
                return True,user
        else:
            return False,"Email Not Found"
    except Exception as e:
        return False,f"Something Wrong in authdb.py: {e}"