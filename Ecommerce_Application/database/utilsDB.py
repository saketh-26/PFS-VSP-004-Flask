from database.connection import DatabaseConnection
from hmac import compare_digest 
#hmac module is to generate and verify keyed-hash
#message authentication codes..

class AuthQueries:
    @staticmethod
    def insertUserRecord(name,email,phone,password_hash):
        with DatabaseConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO USERS(USERNAME,EMAIL,
                    PHONE,HASH_PASSWORD,ROLE,IS_VERIFIED)
                    VALUES(%s,%s,%s,%s,"USER",FALSE)
                    """,(name,email,phone,password_hash),                    
                )
                user_id = cursor.lastrowid
            connection.commit()
            return user_id
    @staticmethod
    def getUserData(email):
        with DatabaseConnection() as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(
                    """SELECT USERID AS userid,
                    USERNAME as username,EMAIL as email,
                    HASHPASSWORD AS hashpassword,
                    ROLE AS role,
                    IS_ACTIVE AS is_active,
                    IS_VERIFIED AS is_verified
                    FROM USERS
                    WHERE EMAIL = %s""",(email,),
                )
            return cursor.fetchone()
    @staticmethod
    def saveVerificationCode(user_id,code_hash):
        with DatabaseConnection() as connection:
            #This query generates and stores a new otp for user
            #while preventing them from requesting new codes
            #too quickly
            with connection.cursor() as cursor:
                cursor.execute(
                    """UPDATE USERS SET OTP_HASH=%s,
                    OTP_EXPIRES_AT=UTC_TIMESTAMP() + 
                    INTERVAL 10 MINUTE,
                    OTP_ATTEMPTS=0 WHERE USER_ID=%s
                    AND ROLE ='USER' AND IS_ACTIVE=TRUE
                    AND IS_VERIFIED=FALSE
                    AND (OTP_EXPIRES_AT IS NULL
                    OR OTP_EXPIRES_AT <= UTC_TIMESTAMP() +
                    INTERVAL 9 MINUTE)""",(code_hash,user_id),)
                saved = cursor.rowcount == 1
                connection.commit()
                return saved
        @staticmethod
        #Email OTP Verification after Registration
        #Finds an Eligble user
        #Locks the user row during the verification
        #Compares the hashes
        #Saves the result
        def verifyCode(user_id,code_hash):
            with DatabaseConnection() as connection:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute(
                        """SELECT OTP_HASH AS otp_hash FROM USERS
                        WHERE USER_ID = %s AND ROLE = 'USER'
                        AND IS_ACTIVE = TRUE
                        AND IS_VERIFIED = FALSE
                        AND OTP_EXPIRES_AT> UTC_TIMESTAMP()
                        AND OTP_ATTEMPTS < 5 FOR UPDATE
                        """,(user_id,),
                    )
                    pending_user = cursor.fetchone()
                    if pending_user is None:
                        return False
                    verified = compare_digest(pending_user['otp_hash'],
                                              code_hash)
                    if verified:
                        cursor.execute(
                            """UPDATE USERS SET IS_VERIFIED = TRUE,
                            OTP_HASH=NULL,
                            OTP_EXPIRES_AT=NULL,
                            OTP_ATTEMPTS=0
                            WHERE USER_ID = %s""",(user_id,),
                        )
                    else:
                        cursor.execute(
                            """UPDATE USERS SET OTP_ATTEMPTS=
                            OTP_ATTEMPTS+1
                            WHERE USER_ID = %s""",(user_id,),
                        )
                    connection.commit()
                    return verified





    

