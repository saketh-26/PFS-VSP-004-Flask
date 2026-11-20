#import mysql.connector as SQLC
import mysql.connector
import os
from pathlib import Path
'''
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
'''
from dotenv import load_dotenv
env_path = Path(__file__).resolve().parents[1]
load_dotenv(env_path)
def DatabaseConnection():
    """Open and return MYSQL Connection"""
    return mysql.connector.connect(
        host=os.environ['DB_HOST'],
        user=os.environ["DB_USER"],
        password=os.environ['DB_PASSWORD'],
        database=os.environ['DB_NAME']
    )