import os
import smtplib
from email.message import EmailMessage
import secrets
import hmac

#This expression generates a cryptogrphicalluy secure 
#6 digit random numeric string with leading zeros if the
#number is smaller than 100,000
def generate_otp():
    return f'{secrets.randbelow(1_000_000):06d}' 
#in above case randbelow is generating 42 --> output becomes
#000042

def otp_hash(user_id,code):
    secret = os.getenv("OTP_SECRET")
    if not secret:
        raise RuntimeError("Set OTP_SECRET in .env")
    message = f"{user_id}:{code}".encode("utf-8")
    return hmac.new(secret.encode("utf-8"),message,
                    "sha256").hexdigest()

def send_verification_email(email,otp):
    """Sending Verification Email"""
    sender = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASSWORD")

    if not sender or not password:
        raise RuntimeError("Set SMTP_USER and Set SMTP_PASSWORD in .env:")
    message = EmailMessage()
    message['From'] = sender
    message['To'] = email
    message['Subject'] = "Verify your ShopZone registration"
    message.set_content(
        f"Your Verification Code is {otp}.It expires in 10 minutes."
    )
    with smtplib.SMTP(
        os.getenv("SMTP_HOST","smtp.gmail.com"),
        int(os.getenv("SMTP_PORT","587")),
        timeout = 15,
    ) as server:
        server.starttls() 
        server.login(sender,password)
        server.send_message(message)
    
