from database.connection import DatabaseConnection

def createTables():
    """Creation of tables"""
    try:
        db_config = DatabaseConnection()
        cursor = db_config.cursor()
        users_table_query = """
        CREATE TABLE IF NOT EXISTS USERS(
        USERID BIGINT AUTO_INCREMENT PRIMARY KEY,
        USERNAME VARCHAR(50) NOT NULL,
        EMAIL VARCHAR(50) NOT NULL UNIQUE,
        HASHPASSWORD VARCHAR(255) NOT NULL,
        ROLE ENUM('ADMIN','USER') DEFAULT 'ADMIN',
        GENDER ENUM('MALE','FEMALE'),
        PHONE VARCHAR(20),
        DATEOFBIRTH DATE,
        PROFILENAME VARCHAR(255),
        PROFILEPATH VARCHAR(255),
        IS_ACTIVE BOOLEAN DEFAULT TRUE,
        CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UPDATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON
        UPDATE CURRENT_TIMESTAMP
        );"""

        products_table_query = """CREATE TABLE IF NOT EXISTS PRODUCTS(
        PRODUCTID BIGINT AUTO_INCREMENT PRIMARY KEY,
        PRODUCTNAME VARCHAR(100) NOT NULL,
        DESCRIPTION TEXT,
        CATEGORY VARCHAR(50),
        QUANTITY INT UNSIGNED DEFAULT O,
        BUYPRICE FLOAT(15,2) DEFAULT 0.0,
        SALEPRICE FLOAT(15,2) DEFAULT 0.0,
        IMGNAME VARCHAR(100),
        STOREDPATH VARCHAR(255),
        IS_ACTIVE BOOLEAN DEFAULT TRUE,
        CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UPDATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON
        UPDATE CURRENT_TIMESTAMP
        );"""

    except Exception as e:
        return f'Something wrong in Database/tables.py : {e}'
    