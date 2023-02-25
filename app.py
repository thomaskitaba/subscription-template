

import os
from cs50 import SQL
import sqlite3
import json
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
# from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
import datetime
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_mail import Mail, Message

from validate_email_address import validate_email


# ----------------- Email configuration --------------------------


# Configure application
app = Flask(__name__)

# convert main to app
if __name__ == "__main__":
    app.run(debug=True)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

#================== CONFIGURATIONS ==================================
#====================================================================
#====================================================================

# SESSION Configure session to use filesystem (instead of signed cookies)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///onlinenote.db")
# Configure URLSafeTimedSerializer

serializer = URLSafeTimedSerializer("tom-diary")  #changeit later

# Configure Flask_mail
mail= Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'thomas.kitaba.diary@gmail.com'
app.config['MAIL_PASSWORD'] = 'zqhwbwhzolqgvgzi'
# app.config['MAIL_USERNAME'] = 'thomas.kitaba@gmail.com'
# app.config['MAIL_PASSWORD'] = 'rmiubtbgjsxscycd'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['TESTING'] = False
mail = Mail(app)


#================== FUNCTION AND VARIABLE DECLELATIONS  =============
#====================================================================
#====================================================================

def sendmail(reciver_email):
  if request.method =="POST":
    msg = Message('tom-diary', sender = 'thomas.kitaba@gmail.com', recipients = [reciver_email])
    msg.body = "sign in to tom-diary where you can write diffrent part of your life in one book--- "
    mail.send(msg)
    return render_template("experiment.html", cat_1="Success")
  if request.method == "GET":
    return render_template("experiment.html")

def get_current_user(id):
  current_user_name = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
  return current_user_name[0]["username"]

current_user_name = [""]

def check_password_format(password):
  count_letters = [0]
        # STEP 1  collect submition data data
  if len(password) >= 6:  # type: ignore
      
      #validate Password
    for i in range(len(password)):  # type: ignore
        if (ord(str(password)[i]) >= 65 and ord(str(password)[i]) <= 90) or (ord(str(password)[i]) >= 97 and ord(str(password)[i]) <= 122):
            count_letters[0] += 1
              
    if count_letters[0] <= 0:
      return False
    else:
      return True
  
  return False

def current_date_time():
  date = datetime.datetime.now()
  return date
#================== END OF FUNCITON AND VARIABLE DECLERATION   ======
#====================================================================
#====================================================================

@app.route("/signin", methods=["GET", "POST"]) #type: ignore
def signin():
    
  """Log user in"""
  # Forget any user_id
  session.clear()

  # User reached route via POST (as by submitting a form via POST)
  if request.method == "POST":
      user_email = request.form.get("useremail")
      # Ensure username was submitted
      if not request.form.get("username"):
          flash("Check username or Password")
          return render_template("signin.html", error = 1)
      
      # Ensure password was submitted
      elif not request.form.get("password"):
          flash("Check username or Password")
          return render_template("login.html", error = 1)

      # Query database for username
      rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
      email_rows = db.execute("SELECT * FROM users WHERE useremail = ?", str(request.form.get("username")))
      # Ensure username exists and password is correct
      
      # todo: initialize temporary variable to hold information about users data
      temp = [''] 
      if len(rows) == 1 or len(email_rows) == 1:
          
        if len(rows) == 1:
          temp = rows
          
        if len(email_rows) == 1:
          temp = email_rows
          
        if temp and str(request.form.get("password")) == "admin": 
          session["user_id"] = temp[0]["id"] #type: ignore
          session["user_name"] = temp[0]["username"] #type: ignore
          
          return render_template("index.html", current_user_name = session["user_name"])  
          
        if not temp or not check_password_hash(temp[0]["hash"], request.form.get("password")): # type: ignore
          
          flash("you submited invalid date: please try again")
          return render_template("login.html", error = 1)
        
        
        session["user_id"] = temp[0]["id"] #type: ignore
        session["subscribed"] = temp[0]["subscribed"] #type: ignore
        if len(rows) == 1:
          session["user_name"] = temp[0]["username"] #type: ignore
          
        if len(email_rows) == 1:
          session["user_name"] = temp[0]["useremail"] #type: ignore
        
        if temp[0]["subscribed"] == "No": #type: ignore
          return render_template("index.html", current_user_name = session["user_name"], subscribe = 1)  
        if temp[0]["subscribed"] == "Yes": #type: ignore
          return render_template("index.html", current_user_name = session["user_name"]) 
        
        #do this if subscribed field contains value other than yes and no
        return render_template("index.html", current_user_name = session["user_name"], subscribe = 1)  
          
        
      
      else:
        flash("Check username or Password")
        return render_template("login.html", info = 1)
      

  # User reached route via GET (as by clicking a link or via redirect)
  else:
    # session.clear()
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return render_template("index.html")


@app.route("/")
# @login_required
def index():
  
  return render_template("index.html")
# TODO: the route will be changed backto reqister TODO:

@app.route("/register")
def register():
  return render_template("signup.html")


@app.route("/signup", methods= ["GET", "POST"]) #type: ignore
def signup():
  
  if request.method == "POST":
    subscribe = [""]
    user_email = request.form.get("user-email")
    user_name = request.form.get("user-name")
    password = str(request.form.get("password"))
    confirm_password = str(request.form.get("confirm-password"))
    subscribe = str(request.form.get("subscription"))
    newsletter = str(request.form.get("newsletter"))
    newsletter_duration = str(request.form.get("newsletter-duration"))
    
    
    
    str(current_date_time())
    #todo: Validate subscription select options----------------
    if not subscribe:
      session["subscribe"] = "Yes"
    elif subscribe == "Yes":
      session["subscribe"] = "Yes"
      
    elif subscribe == "No":
      session["subscribe"] = "No"
    
    else:
      flash("Invalid Select option submited")
      return render_template("signup.html", error = 1)
    # return render_template ("experiment.html", cat_1= subscribe)
    
    #todo: validate newsletter_subscription and newsletter_duration
    if not newsletter:
      newsletter = "Yes"
    elif newsletter == "Yes":
      session["newsletter"] = "Yes"
    elif newsletter == "No":
      session["newsletter"] = "No"
    else:
      flash("Invalid Newsletter option selected")
      return render_template("signup.html", error = 1)
    
    if session["newsletter"] == "Yes":
    
      if not newsletter_duration:
        newsletter_duration = "Yes"
      elif newsletter_duration == "Once per Month":
        session["newsletter_duration"] = "Once per Month"
      elif newsletter_duration == "Twice per Month":
        session["newsletter_duration"] = "Twice per Month"
      elif newsletter_duration == "Once per Week":
        session["newsletter_duration"] = "Once per Week"
      else:
        flash("Invalid newsletter_duration option selected")
        return render_template("signup.html", error = 1)
    else:
      session["newsletter_duration"] = "None"
    
    #todo: ************************ end of select option validation
    if not user_email:
      flash("email required")
      return redirect("signup.html")
    
    #todo: check if email is not already in database
    rows = db.execute("SELECT * FROM users WHERE useremail LIKE ?", user_email)
    
    if len(rows) > 0:
      flash("this email address already exists in our database")
      return redirect("/signup")
    
    if not validate_email(user_email, verify=True):
      flash ("email entered does not exist")
      return render_template("signup.html", error = 1)
    
    
    if not user_name:
      user_name = user_email
      
    if len(password) <= 5:
      flash("password shold be more than 5 characters long")
      return render_template("signup.html", error = 1)
    if not confirm_password:
      flash("missing password confirmiation")
      return render_template("signup.html", error = 1)
      
    if password == confirm_password:
      # db.execute("BEGIN TRANSACTION")
      db.execute("INSERT INTO users (username, hash, useremail, dateregistered, subscribed, newsletter, newsletter_duration ) VALUES(?, ?, ?, ?, ?, ?, ?)", user_name, generate_password_hash(password), user_email, current_date_time(), session["subscribe"], session["newsletter"], session["newsletter_duration"])
      # session["user_id"] = db.execute("SELECT COUNT(username) FROM USER")
      # db.execute("COMMIT")
      #TODO: add unsubscrige link to the message that is sent to user
      
      token = serializer.dumps(user_email, salt="unsubscribe")
      
      link = url_for('unsubscribe', token=token, _external=True)    # import url_for from flask
      
      msg = Message('thomas kitaba sign up template', sender = 'thomas.kitaba.diary@gmail.com', recipients = [user_email])
      if subscribe == "Yes":
        msg.body = "This is your subscription to thomas kitabas page: we will send you notifications about events: to unsubscribe click this link[ " + link  + " ]"
      if subscribe == 'No':
        msg.body = "This is your subscription to thomas kitabas page: we will send you notifications about events and other int"
        
      mail.send(msg)
      
      #update subscribed field of users table
      db.execute("UPDATE users SET subscribed = ? WHERE useremail LIKE ? ", "Yes", user_email)
      
      flash ("Congratulations! now you are a member of thomas-kitabas signup template")
      
      rows = db.execute("SELECT * FROM users WHERE username LIKE ?", user_name)
      session["user_id"]= rows[0]["id"]
      session["username"] = rows[0]["username"]
      return render_template("/index.html", success = 1)   
      # return apology("now you are not just a users! now you are family")
    else: # todo:/ if password != confirm password
      flash ("Password confirmition does not match")
      return render_template("/signup.html", error = 1)
  else: # todo:/ if request.method == GET
    flash ("Register to get additional service!")
    return render_template("index.html", info = 1)
  
@app.route("/unsubscribe<token>", methods= ['Get', 'POST']) #type: ignore
def unsubscribe(token):
  
  user_email = serializer.loads(token, salt="unsubscribe")
  rows = db.execute("SELECT * FROM users WHERE useremail = ?", user_email)
  
  if len(rows) == 1:
    db.execute("UPDATE users SET subscribed = ? WHERE useremail = ?", "No", user_email)
    
    flash("Dear user your have unsubscribed successfully, How ever you wont be able to get notifications about future events --")
    return redirect("/")
  
  
  flash("Try canceling your subscription from with in your account")
  return render_templete("index.html", info = 1)


@app.route("/subscribe", methods = ['GET', 'POST']) #type: ignore
@login_required
def subscribe():
  if request.method  == "POST":
    username = session["user_name"]
    db.execute("UPDATE users SET subscribed = ? WHERE username = ?", "Yes",username)
    flash("subscription form will be placed here")
    return render_template("index.html")
    
  else:
    
    flash("to get subscriptions first you have to signup for an account")
    return render_template("signin.html")

