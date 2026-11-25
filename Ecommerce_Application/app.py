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
app.secret_key = os.getenv("OTP_SECRET")
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
    name = request.form.get("name","").strip()
    email = request.form.get("email","").strip().lower()
    phone = request.form.get("phone","").strip()
    password=request.form.get("password","")
    confirm_password = request.form.get("confirm_password","")
    if not name or len(name) > 50 or len(phone) >20:
        flash("Enter a name upto 50characters and a phone"
        "number up to 20characters","danger")
        return redirect(url_for('register'))
    #regex match -->basic structure of an email
    #[^\s@] --> one or more characters excluding whitespace and @
    if len(email)>50 or not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+",email):
        flash("Enter a valid email address","danger")
        return redirect(url_for('register'))
    if password!=confirm_password:
        flash("Passwords dont match","danger")
        return redirect(url_for('register'))
    password_hash = bcrypt.hashpw(password.encode("utf-8"),
                                  bcrypt.gensalt()).decode("ascii")
    try:
        user_id=AuthQueries.insertUserRecord(
            name,email,phone or None,password_hash
        )
    except Error as error:
        if error.errno == errorcode.ER_DUP_ENTRY:
            flash("Email is already registered.Log in to continue","info")
            return redirect(url_for("login"))
        app.logger.exception("Couldnot create a user")
        flash("Registration failed.Please try again","danger")
        return redirect(url_for("register"))
    session.clear()
    session['pending_verification'] = {"id":user_id,"email":email}
    send_registration_code(user_id,email)
    return redirect(url_for("verify"))    

@app.route('/verify',methods=['GET','POST'])
def verify():
    pending = session.get("pending verification")
    if not pending:
        return redirect(url_for("login"))
    if request.method=="GET":
        return render_template("verify.html",
                               email=pending['email'])
    code = request.form.get("otp","").strip()
    if not re.fullmatch(r"[0-9]{6}",code):
        flash("Enter the Six-digit code from your email,",
              "danger")
        return redirect(url_for("verify"))
    user_id = pending["id"]
    try:
        verified = AuthQueries.verifyCode(user_id,
                                          otp_hash(user_id,code))
    except Error:
        app.logger.exception("Could not verify the user")
        flash("Verification failed..Please try again later",
              "danger")
        return redirect(url_for("verify"))
    if not verified:
        flash("The Code is incorrect,expired or out of attempts",
              "danger")
        return redirect(url_for("verify"))
    session.pop("pending_verification",None)
    flash("Email Verified.You can login","success")
    return redirect(url_for("login"))    

@app.post("/verify/resend")
def resend_verification():
    pending = session.get("pending_verification")
    if not pending:
        return redirect(url_for("login"))
    send_registration_code(pending["id"],pending["email"])
    return redirect(url_for("verify"))

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    email = request.form.get("email","").strip().lower()
    password = request.form.get("password","").encode("utf-8")
    try:
        user = AuthQueries.getUserData(email)
    except Error:
        app.logger.exception("Couldnot lokup user")
        flash("Login is temporarily unavailable","danger")
        return redirect(url_for("login"))
    if not user or not password or len(password) > 72 or not bcrypt.checkpw(
        password,user["hashpassword"].encode("ascii")):
        flash("Incorrect email or password","danger")
        return redirect(url_for("login"))
    if not user["is_active"]:
        flash("This account is inactive","danger")
        return redirect(url_for("login"))
    role=user['role'].upper()
    session.clear()
    if not user["is_verified"]:
        if role == "USER":
            session["pending_verification"] = {
                "id":user['userid'],
                "email":user["email"]
            }
            send_registration_code(user["userid"],user["email"])
            return redirect(url_for("verify"))
        flash("This accoount requires setup","danger")
        return redirect(url_for("verify"))
    session["id"] = user["userid"]
    session["name"] = user["username"]
    session["email"] = user["email"]
    session["role"] = role
    return redirect(url_for("products"))

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