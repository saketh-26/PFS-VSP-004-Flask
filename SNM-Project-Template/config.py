#This file will be useful for establishing configurations

from dotenv import load_dotenv
import os
load_dotenv()

class Config():
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")
    from_email = os.getenv("FROM_EMAIL")
    email_app_password = os.getenv("EMAIL_APP_PASSWORD")
    #print(db_host,db_port,db_user,db_password,db_name)

class emailTemplates():
    def send_otp_template(otp:int,username:str):
        template = f"""Hi {username},
        Welcome to **SNS**!
        To complete your registration,
        please use the One-Time Password below:
        **Your OTP is: {otp}**
        This OTP is valid for **3 minutes**.Please don't share 
        this code with anyone.If you didnot request this registration,
        you can safely ignore this email.
        
        Best regards,
        **SNS Team**
        """
        return template

    def send_reset_password_template(username:str,
                                     url:str,
                                     time:int):
        template=f"""Hi {username}
        We have received a request to reset the password for your
        ***SNS** account.To reset your password,please click
        the below:
        reset URL: {url}
        This password reset link is valid for 
        **{time} minutes**.Please donot share this link with anyone.
        If you didnot request a password reset,you can safely ignore
        this email.
        Best regards,
        **SNS Team**
        """
        return template

