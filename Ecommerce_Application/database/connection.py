import mysql.connector as SQLC

def DatabaseConnection():
    try:
        db_config = SQLC.connect(
            host="localhost",
            user = "root",
            password="chinnu",
            database="ecommerce"
        )
        return db_config
    except Exception as e:
        return f"Something wrong in Database Connection : {e}"