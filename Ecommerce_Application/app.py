import os,re
import smtplib
import uuid 
import bcrypt
from pathlib import Path
from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
    abort,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from mysql.connector import Error,errorcode
from database import AuthQueries,createTables
from utils import send_verification_email,generate_otp,otp_hash

load_dotenv(Path(__file__).with_name(".env"))
app = Flask(__name__) 
app.secret_key = os.getenv("SECRET_KEY")
if not app.secret_key:
    raise RuntimeError("Set SECRET_KEY in .env before " \
    "starting the app.")
#"Lax" -->This config will restricts whenthe browser sends
#your session cookie on cross-site requests
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
(Path(app.static_folder)/ "images" / "products").mkdir(
    parents=True,exist_ok=True
)
@app.route('/')
def home():
    return render_template("home.html")

def send_registration_code(user_id,email):
    otp= generate_otp()
    try:
        saved = AuthQueries.saveVerificationCode(
            user_id,otp_hash(user_id,otp))
    except Error:
        app.logger.exception("Could not save Registration OTP")
        flash("Could not save the code in MYSQL." \
        "Check the Flask terminal")
        return
    if not saved:
        flash("use your latest code or wait for sometime")
        return
    try:
        send_verification_email(email,otp)
    except smtplib.SMTPAuthenticationError:
        app.logger.exception("Gmail Rejected the SMTP login")
        flash("Gmail rejected the login..Check App Password")
    except (KeyError,RuntimeError,ValueError):
        app.logger.exception("Invalid Email Configuration")
        flash("Check the SMTP Settings in .env and be careful",
              "danger"
              )
    except OSError:
        app.logger.exception("Could not send registration OTP")
        flash("Email delivery failed")
    else:
        flash("We mailed you a six-digit verification code.",
              "success")
    
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == "GET":
        return render_template("register.html")

@app.route("/products")
def products():
    return render_template("user/products.html")
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))
if __name__ == "__main__":
    print(createTables())
    app.run(host="0.0.0.0",
            port=5002,debug=True)