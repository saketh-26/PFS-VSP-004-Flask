import os
import smtplib
from email.message import EmailMessage

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
    
