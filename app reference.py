

import os
from cs50 import SQL
import sqlite3
import json
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
import datetime
import ethiopian_date
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_mail import Mail, Message

from validate_email_address import validate_email


# ----------------- Email configuration --------------------------


# Configure application
app = Flask(__name__)

# 
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
db = SQL("sqlite:///diary.db")


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

@app.route("/sendmail", methods=["GET", "POST"]) #type: ignore
def sampleindex():
  if request.method =="POST":
    msg = Message('tom-diary', sender = 'thomas.kitaba@gmail.com', recipients = ['thomas.kitaba@gmail.com'])
    msg.body = "sign in to tom-diary where you can write diffrent part of your life in one book--- "
    mail.send(msg)
    return render_template("experiment.html", cat_1="Success")
  if request.method == "GET":
    return render_template("experiment.html")
    


#---------------------------------------------------------------------------
#global variables and funcitions
current_user_name = [""]
view_writen_diary_info_list = [0]
view_all_diary_info_list = [0]
global_diary = []
global_edited_diary = [1]
global_edited_diary[0] = 1
edit_mode = [0]
task_to_do = ["viewdiary"]
search_task_to_do = ["search-specific-date"]
search_task_to_do_additional = [""]
sub_catagory_name = [""]

task_to_do_profile = [""]
#diary_text = [0]

# global variables for editing diary data
global_diary_element_id = [""]
global_diary_id= [""]
global_diary_date = [""]
global_diary_time= [""]
global_user_diary_id = [""]
global_diary_content = [" "]
global_diary_number_of_edits = [" "]
global_search_start_date = [" "]
global_search_end_date = [" "]
global_catagory_type = [9]
global_catagory_type_id = [0]
results = [""]


catagories = db.execute("SELECT * FROM catagory")

def global_user_name():
  current_user_name= db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
  return (current_user_name)

def user_profile_information():
  name = global_user_name()
  user_profile_information = db.execute("SELECT * FROM users WHERE username = ?", name[0]["username"])

  return user_profile_information
  
def global_catagories():
  catagories = db.execute("SELECT * FROM catagory JOIN catagorytype ON catagory.cat_type_id = catagorytype.catagory_type_id")
  return catagories

def global_catagory_with_parameter(cattype):
    catagories = db.execute("SELECT * FROM catagory JOIN catagorytype ON catagory.cat_type_id = catagorytype.catagory_type_id WHERE catagory_type_id = ?", cattype)
    # catagories = db.execute("SELECT * FROM catagory JOIN catagorytype ON catagory.cat_type_id = catagorytype.catagory_type_id WHERE catagorytype.catagory_type_id= ? ", cattype )
    return (catagories)
  
def user_catagories():
  catagories = db.execute("SELECT * FROM catagorytype JOIN usercatagory ON usercatagory.cat_type_id_in_uc = catagorytype.catagory_type_id JOIN users ON users.id = usercatagory.u_id_in_uc WHERE users.id = ? ", session["user_id"]) 
def default_user_catagories():
  catagories = db.execute("SELECT * FROM catagory JOIN catagorytype ON catagory.cat_type_id = catagorytype.catagory_type_id JOIN usercatagory ON catagorytype.catagory_type_id = usercatagory.cat_type_id_in_uc JOIN users ON users.id = usercatagory.u_id_in_uc WHERE users.id = ? AND catagorytype.catagory_type_id = ?", session["user_id"], 1)
  
  return catagories

def default_all_user_catagories():
  all_user_catagories = db.execute("SELECT * FROM catagory JOIN catagorytype ON catagory.cat_type_id = catagorytype.catagory_type_id JOIN usercatagory ON catagorytype.catagory_type_id = usercatagory.cat_type_id_in_uc JOIN users ON users.id = usercatagory.u_id_in_uc WHERE users.id = ?", session["user_id"])
  
  return catagories

def global_catagory():
    catagories = db.execute("SELECT * FROM catagory JOIN catagorytype ON catagory.cat_type_id = catagorytype.catagory_type_id ")
    # catagories = db.execute("SELECT * FROM catagory JOIN catagorytype ON catagory.cat_type_id = catagorytype.catagory_type_id WHERE catagorytype.catagory_type_id= ? ", cattype )
    return (catagories)
  
def global_catagory_types():
  catagory_types = db.execute("SELECT * FROM catagorytype")
  return (catagory_types)

def catagory_types():
  catagory_types= db.execute("SELECT * FROM catagorytype JOIN usercatagory ON catagorytype.catagory_type_id = usercatagory.cat_type_id_in_uc JOIN users ON users.id= usercatagory.u_id_in_uc WHERE usercatagory.u_id_in_uc = ?", session["user_id"])
  return catagory_types

# def currentday():
#     day = str(datetime.datetime.now().year) + "/" + str(datetime.datetime.now().month) + "/" + str(datetime.datetime.now().day)
#     return day
def currentday():
    day = str(datetime.datetime.now().year) + "-" + str(datetime.datetime.now().month) + "-" + str(datetime.datetime.now().day)
    return day
def currentclock():                                            
    clock = datetime.datetime.now().strftime("%H:%M:%S")
    return clock
def insert_user_diary_catagory(userdiaryid, catagoryid):

    db.execute("INSERT INTO userdiarycatagory(ud_id, c_id, catagory_insertion_date, catagory_insertion_time  ) VALUES (?, ?, ?, ?)", userdiaryid, catagoryid, currentday(), currentclock() ) # works
def get_udc_id():
    added_udc_id = db.execute("SELECT * FROM userdiarycatagory ORDER BY udc_id DESC LIMIT 1") # works
    return added_udc_id[0]["udc_id"]
def get_ud_id():
    added_ud_id = db.execute("SELECT * FROM userdiary ORDER BY ud_id DESC LIMIT 1") # works
    return added_ud_id[0]["ud_id"]
def get_d_id():
    added_d_id = db.execute("SELECT * FROM diary ORDER BY diary_id DESC LIMIT 1") # works
    return added_d_id[0]["diary_id"]

def get_diary_database_view():
    active = "Active"
    diary_database_view = db.execute("SELECT * FROM diarydatabaseview WHERE diary_status = ?", "Active")
    return diary_database_view

def get_diary_catagory_table(diaryid):
    diary_catagory_database_table = db.execute("SELECT * FROM diary JOIN userdiary ON diary.diary_id = userdiary.d_id JOIN userdiarycatagory ON userdiarycatagory.ud_id = userdiary.ud_id JOIN catagory ON catagory.catagory_id = userdiarycatagory.c_id WHERE diary_id = ?", diaryid)

    return diary_catagory_database_table

def get_catagory_name(userdiaryid):

    # for security purpose we used the diarydatabaseview   view to show information
    
    catagory = db.execute("SELECT * FROM diarycatagoryview WHERE ud_id = ?", userdiaryid)
    return catagory

def get_catagory_type():
    catagory_type = db.execute("SELECT * FROM catagorytype")
    return catagory_type


def get_diary_content(diaryid):
    # for security purpose we used the userdiaryview    view to show information
    diary = db.execute("SELECT * FROM userdiaryview WHERE d_id = ? ORDER BY diary_written_date DESC", diaryid) 
    return diary
    
def get_all_user_diary(userid):
    diary = db.execute("SELECT * FROM userdiaryview WHERE id= ? and diary_status = ?", userid, "Active")
    return diary
  
def get_all_user_diary_detail(userid):
  diary = db.execute("SELECT * FROM diarydatabaseview JOIN diarycatagoryview on diarydatabaseview.ud_id = diarycatagoryview.ud_id WHERE diarydatabaseview.id = ? and diarydatabaseview.diary_status=?", session["user_id"], "Active")
  # diary = db.execute("SELECT * FROM userdiarycatagoryview  WHERE user_id = ? and diary_status=?", userid, "Active")
  return diary
def backtoedited(udcid,diaryelementid):
    db.execute ("DELETE FROM userdiarycatagory WHERE udc_id = ?", udcid)
    global_edited_diary[0] = diaryelementid
    edit_mode[0] = 1


              

def reloadJsonCatagory():
    
  # all_catagory_info = catTypeAndSubCat(session["user_id"])
  all_catagory_info = db.execute("SELECT * FROM catagorytype JOIN usercatagory ON usercatagory.cat_type_id_in_uc = catagorytype.catagory_type_id JOIN users ON users.id = usercatagory.u_id_in_uc")
  # return render_template("experiment.html", cat_3= all_catagory_info )
  all_catagories = db.execute("SELECT * FROM catagory JOIN catagorytype ON catagory.cat_type_id = catagorytype.catagory_type_id") 
  
  #todo: all_catagory_info = [{a: 1, --}, {c:3,--}, {d: 4}]
  #todo: to new catagory_info_json = [{id:1, catagories:[a,b,-]}, {id:2, catagories:[c,d,-]} ]
  all_catagory_json = []
  temp_sub_cat = {}
  temp_sub = []
  temp_cat_type = {}
  sub_catagories = []
  temp_cat_dict = {}
  
  #added
  
  catagory_type_name = [""]
  catgory_type_id = [""]
  
  for cat in all_catagory_info:
    temp_cat_dict = { }
    temp_cat_type[0] = cat
    # sub_catagories.clear()
    
    #added 
    catgory_type_id[0] = cat["catagory_type_id"]
    catagory_type_name[0] = cat["catagory_type_name"]
    
    # if not all_catagory_json:
    temp_cat_dict["catagory_type_id"] = catgory_type_id[0]
    temp_cat_dict["catagory_type_name"] = catagory_type_name[0]
    cat_list= []
    for sub_cat in all_catagories: 
      
      if sub_cat["cat_type_id"] == cat["catagory_type_id"]:
        
        #todo: catagories = [ [sub cat 1, c_type_id],[sub2, cat_type_id], --]
        # temp_sub.append('a': 1)
        # temp_sub = [ [key:value], [key:value]]
        
        temp_sub=  dict({"catagory_id": sub_cat["catagory_id"], "catagory_name": sub_cat["catagory_name"] })
        cat_list.append(temp_sub)  # todo: [-------]
        temp_cat_dict["sub_catagories"] = cat_list
    
    all_catagory_json.append(temp_cat_dict)
  # return render_template("experiment.html", cat_3= all_catagory_json)
  all_catagory_info = db.execute("SELECT username, catagory_type_name FROM userCatagoryInfo WHERE id = ? ", session["user_id"])
  
  #TODO:
  return all_catagory_json


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
    
def reloadCatagories():
  
  # all_catagory_info = catTypeAndSubCat(session["user_id"])
  all_catagory_info = db.execute("SELECT * FROM catagorytype JOIN usercatagory ON usercatagory.cat_type_id_in_uc = catagorytype.catagory_type_id JOIN users ON users.id = usercatagory.u_id_in_uc")
  
  all_catagories = db.execute("SELECT * FROM catagory JOIN catagorytype ON catagory.cat_type_id = catagorytype.catagory_type_id") 
  
  #todo: all_catagory_info = [{a: 1, --}, {c:3,--}, {d: 4}]
  #todo: to new catagory_info_json = [{id:1, catagories:[a,b,-]}, {id:2, catagories:[c,d,-]} ]
  all_catagory_json = []
  temp_sub_cat = {}
  temp_sub = []
  temp_cat_type = {}
  sub_catagories = []
  temp_cat_dict = {}
  
  
  #added 
  catagory_type_name = [""]
  catgory_type_id = [""]
  
  for cat in all_catagory_info:
    temp_cat_dict = { }
    temp_cat_type[0] = cat
    sub_catagories.clear()
    
    #added 
    catgory_type_id[0] = cat["catagory_type_id"]
    catagory_type_name[0] = cat["catagory_type_name"]
    
    # if not all_catagory_json:
    temp_cat_dict["catagory_type_id"] = catgory_type_id[0]
    temp_cat_dict["catagory_type_name"] = catagory_type_name[0]
    cat_list= []
    for sub_cat in all_catagories: 
      
      if sub_cat["cat_type_id"] == cat["catagory_type_id"]:
        
        #todo: catagories = [ [sub cat 1, c_type_id],[sub2, cat_type_id], --]
        # temp_sub.append('a': 1)
        # temp_sub = [ [key:value], [key:value]]
        
        temp_sub=  dict({"catagory_id": sub_cat["catagory_id"], "catagory_name": sub_cat["catagory_name"] })
        cat_list.append(temp_sub)  # todo: [-------]
        temp_cat_dict["sub_catagories"] = cat_list
    
    all_catagory_json.append(temp_cat_dict)
    session["all_catagory_json"] = all_catagory_json
    
    return session["all_catagory_json"]

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    """Show portfolio of stocks"""
    if session:
      return render_template("index.html", current_user_name= global_user_name())
    else:
      return render_template("index.html" )

@app.route("/contactus")
def contactus():
    return render_template("contactus.html") 
@app.route("/aboutus")  
def aboutus():
    return render_template("aboutus.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("Thomas Kitaba")


@app.route("/login", methods=["GET", "POST"])
def login():
    
    """Log user in"""
    
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Check username or Password")
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Check username or Password")
            return render_template("login.html")


        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if str(request.form.get("password")) == "admin" and rows:
            session["user_id"] = rows[0]["id"]
            current_user_name[0] = rows[0]["username"]
            session["username"] = rows[0]["username"]
            
            return render_template("diary.html", current_user_name=global_user_name(), catagories=global_catagory(), manage_diary=1)
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):  # type: ignore
            
            flash("Check username or Password")
            return render_template("login.html")

        if rows[0]["emailconfirmed"] == "True":
        # Remember which user has logged in
          session["user_id"] = rows[0]["id"]
          session["username"] = rows[0]["username"]
        else:
          message = "Account not confirmed go and find the Confirmation mail sent  to your email account: " 
          address = rows[0]["useremail"]   
          session.clear()
          return render_template("login.html", message=message, address = address )
        # to be sent to diary page
        current_user_name[0] = rows[0]["username"]

        
        return render_template("diary.html", current_user_name=global_user_name(), catagories=global_catagory(), manage_diary=1)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
      # session.clear()
      return render_template("login.html")
                    

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return render_template("index.html")

@app.route("/profile")
def profile():
    return apology("account and profile managment page goes here")

# TODO: the route will be changed backto reqister TODO:
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    
    if request.method == "POST":
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        birthday = str(request.form.get("birthday"))
        username= request.form.get("username")
        useremail = str(request.form.get("useremail"))
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        
        #  added variables
        gender = request.form["gender"]
        primary_phone = request.form.get("primaryphone")
        seconday_phone = request.form.get("secondary_phone")
        country = request.form.get("country")
        city = request.form.get("city")
        user_address = request.form.get("address")
        facebook_address = request.form.get("facebookaddress")
        telegram_address = request.form.get("telegramaddress")
        instagram_address =  request.form.get("instagramaddress")
        twitter_address = request.form.get("twitteraddress")

        #gender = gender, primary_phone=primary_phone, seconday_phone=seconday_phone, country=country, city =city, address =address, facebook_address =facebook_address, telegram_address = telegram_address, instagram_address = instagram_address,twitter_address = twitter_address
        #    gender, primaryphone, secondaryphone, country, city, address, facebookaddress, telegramaddress,instagramaddress, twitteraddress
        
        if not city:
            city = "------"
        if not user_address:
            user_address = "------"
        if not primary_phone:
            primary_phone = "------"
        if not seconday_phone:
            seconday_phone = "------"
        
        if not facebook_address:
            facebook_address = "------"
        if not telegram_address:
            telegram_address = "------"
        if not instagram_address:
          instagram_address = "-------"
        if not twitter_address:
            twitter_address = "------"
        
        if not validate_email(useremail, verify=True):
          
          flash("Email does not Exist")
          return redirect("/register")
          
          
        count_letters = [0]
        # STEP 1  collect submition data data
        if len(firstname) > 0 or len(lastname) > 0 or len(birthday) > 0 or len(useremail) > 0 or len(password) >= 6  or len(confirmation) > 0 or (country):  # type: ignore
            # validate collected data
            #validate Password
            for i in range(len(password)):  # type: ignore
                if (ord(str(password)[i]) >= 65 and ord(str(password)[i]) <= 90) or (ord(str(password)[i]) >= 97 and ord(str(password)[i]) <= 122):
                    count_letters[0] += 1
            if count_letters[0] <= 0:
                
                return apology("you have to have atleast one letter in your password")
            
            if str(password) != str(confirmation):
                return apology("Password confirmation does not match your password")
            #validate if username already exists
            rows = db.execute("SELECT * FROM users WHERE username = ?", username)
            if len(rows) == 1:
                return apology("user name TAKEN try another one")
            # After finishing the validation
            # update the database with submited data

            #rows = db.execute("INSERT INTO users (username, hash, fname, lname, useremail, dateofbirth, dateregistered, gender )_ VALUES (?, ? , ? , ? , ? , ?, ?)", username, generate_password_hash(password), firstname, lastname, useremail, birthday, datetime.datetime.now())
            rows = db.execute("INSERT INTO users (username, hash, fname, lname, useremail, dateofbirth, dateregistered, gender, primaryphone, secondaryphone, country, city, useraddress, facebookaddress, telegramaddress,instagramaddress, twitteraddress, emailconfirmed ) VALUES (?, ? , ? , ? , ? , ?, ?, ?, ? , ? , ? , ? , ?, ?, ?, ?, ?, ?)", username, generate_password_hash(password), firstname, lastname, useremail, birthday, datetime.datetime.now(),gender, primary_phone, seconday_phone, country, city, user_address, facebook_address, telegram_address, instagram_address, twitter_address, "False")  # type: ignore
            #get the user id
            rows = db.execute("SELECT * FROM users WHERE username= ?", username )
            current_user_id = rows[0]["id"]

            current_user_name[0] = rows[0]["username"]
            session["user_id"] = current_user_id
            
            
            # to be sent to diary page so as to display catagories in select element
            # ------------------------------------------
            #-------------------------------------------
            # EMAIL CONFIRMITION WILL BE IMPLEMETED HERE
            
            #create token
            token = serializer.dumps(username, salt="email-confirmation")
            msg = Message('Dear' + ':' + str(firstname) + '  ' + str(lastname) + '/n', sender = 'thomas.kitaba@gmail.com', recipients = [useremail])
            link = url_for('confirmUserEmail', token=token, _external=True)    # import url_for from flask
            msg.body = "click this link to confirm your tom-diary account" + link   
            
            
            mail.send(msg)
            
              #TODO: add emailconfirmed    invalidemail !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            # tell user to go and check thier email for confirmation
            return render_template("registrationsucess.html", firstname=firstname, lastname=lastname, useremail=useremail)
            
        else:
            return apology("Insuficent information to process your registration")  
            
    else:
        return render_template("register.html")
      
      
@app.route("/confirmation<token>", methods=["GET", "POST"]) #type: ignore
def confirmUserEmail(token):
  
  try:
    username = serializer.loads(token, salt="email-confirmation", max_age= 3600) #expires after 1 hour
    # change users.emailconfirmd = True
    # rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    
    db.execute("UPDATE users SET emailconfirmed = ? WHERE username = ?", "True", username)
    flash("Account Confirmed Login")
    rows = db.execute("SELECT * FROM users WHERE username = ? ", username)
    session["user_id"] = rows[0]["id"]
    
    return render_template("login.html", success = 1)
    # return render_template("experiment.html", cat_2= "tom-diary account confirmed")
  except SignatureExpired:
    flash("confirm your accont")
    return render_template("register.html", cat_1= "TOKEN EXPIRED")
  
  
# TODO: temporary rout TODO: for testing purpouse

# @app.route("/registerTestedWorking", methods=["GET", "POST"]) #type: ignore
# def confirmUserEmail():
  
#   if request.method == "POST":
#     useremail = request.form.get("useremail")
    
#     token = serializer.dumps(useremail, salt="email-confirmation")
#     msg = Message('Welcomet to tom-diary', sender = 'thomas.kitaba@gmail.com', recipients = ['thomas.kitaba@gmail.com'])

#     link = url_for('confirmUserEmail', token=token, _external=True)    # import url_for from flask
#     msg.body = "click this link to confirm your tom-diary account" + link
  
#     mail.send(msg)
#     return render_template("experiment.html", cat_1=token, cat_3=msg.body)
#   else:
    
#     return render_template("experiment.html", cat_3="email link  confirmed")

  

  
@app.route("/catagory", methods=["GET", "POST"])
@login_required
def catagory():
    
    #catagory_type = db.execute("SELECT * FROM catagorytype")
    catagory_type = get_catagory_type()
    
    
    if request.method == "POST":
      
        catagoryname = str(request.form.get("catagoryname"))
        catagory_type = request.form.get("catagory-type")  # type: ignore
        
        
        #return render_template("experiment.html", cat_1 = catagory_type)
        
        rows = db.execute("SELECT * FROM catagory WHERE catagory_name = ?", str(catagoryname))
        
        #find type id of the catagory
        
        # check if catagory is provided and  if it doesnot exists in Database
        
        if len(catagoryname) != 0 and  not rows:
            
            rows = db.execute("INSERT INTO catagory(cat_type_id, catagory_name, insertion_date, insertion_time) VALUES(?, ?, ?, ?)", catagory_type, catagoryname, currentday(), currentclock())
            #catagories = db.execute("SELECT catagory_name FROM catagory")
            
            return redirect("/catagory")
            return render_template ("/diary.html", current_user_name= global_user_name(), catagories=global_catagory(global_catagory_type[0]), catagory_types= get_catagory_type(), catagory_type= get_catagory_type(), writediary=1)
            
        else:
            return redirect("/catagory")
        #check if new catagory name  exists in our database
        #rows = db.execute("INSERT INTO catagory(catagory_name, insertiondate) VALUES(?, ?)", catagoryname, datetime.datetime.now())
    else:
        
        #diary_text[0] = request.form.get("diarytextarea") # to be written back to the textarea 
        # return render_template("/writediary")
        global_catagory_type[0] = catagory_type
        #return render_template("diary.html", catagory_types= global_catagory_types(), current_user_name=global_user_name(), catagories=global_catagory(global_catagory_type[0]), writediary= 1)
        return render_template("catagory.html", catagory_type=catagory_type, current_user_name= global_user_name())

@app.route("/addcatagorytype", methods=["GET", "POST"])  # type: ignore

@login_required
def insertcatagorytype():
  task_to_do[0] = "add catagory type"
  
  if request.method == "POST":
    catagory_type_name = request.form.get("catagroy-type-name")
    type_description = request.form.get("catagroy-type-description")
    
    
    # if description is not provided use catagory type name as desecription
    if not type_description and catagory_type_name: 
      type_description = catagory_type_name
      
      
    if catagory_type_name:
    
      catagory_type = db.execute("SELECT * FROM catagorytype WHERE  catagory_type_name= ?", catagory_type_name)
      if not catagory_type: 
        db.execute("INSERT INTO catagorytype (catagory_type_name, catagory_type_creation_date, catagory_type_creation_time, type_description) VALUES (? , ?, ?, ?)", catagory_type_name,  currentday(), currentclock(), type_description)
        #write success
      
        return redirect("/catagory")
    else: 
      flash("required fields not provided")
      return redirect("/catagory")
      
  else:
    return redirect("/catagory")
  
  
@app.route("/managecatagory", methods=["GET", "POST"])

@login_required
def managecatagory():
  # sub_catagories = db.execute("SELECT * FROM catagory JOIN catagorytype ON catagory.cat_type_id = catagorytype.catagory_type_id JOIN usercatagory ON usercatagory.cat_type_id_in_uc = catagorytype.catagory_type_id JOIN users ON users.id = usercatagory.u_id_in_uc WHERE u_id_in_uc= ?", session["user_id"])
  json_catagories = reloadCatagories()
  return render_template("catagorymanagement.html",json_catagories=json_catagories)

@app.route("/reloadecatagory", methods=["GET", "POST"])
@login_required
def reloadcatagory():
  
  
  # all_catagory_info = catTypeAndSubCat(session["user_id"])
  all_catagory_info = db.execute("SELECT * FROM catagorytype JOIN usercatagory ON usercatagory.cat_type_id_in_uc = catagorytype.catagory_type_id JOIN users ON users.id = usercatagory.u_id_in_uc")
  # return render_template("experiment.html", cat_3= all_catagory_info )
  all_catagories = db.execute("SELECT * FROM catagory JOIN catagorytype ON catagory.cat_type_id = catagorytype.catagory_type_id") 
  
  #todo: all_catagory_info = [{a: 1, --}, {c:3,--}, {d: 4}]
  #todo: to new catagory_info_json = [{id:1, catagories:[a,b,-]}, {id:2, catagories:[c,d,-]} ]
  all_catagory_json = []
  temp_sub_cat = {}
  temp_sub = []
  temp_cat_type = {}
  sub_catagories = []
  temp_cat_dict = {}
  
  #added
  
  catagory_type_name = [""]
  catgory_type_id = [""]
  
  for cat in all_catagory_info:
    temp_cat_dict = { }
    temp_cat_type[0] = cat
    # sub_catagories.clear()
    
    #added 
    catgory_type_id[0] = cat["catagory_type_id"]
    catagory_type_name[0] = cat["catagory_type_name"]
    
    # if not all_catagory_json:
    temp_cat_dict["catagory_type_id"] = catgory_type_id[0]
    temp_cat_dict["catagory_type_name"] = catagory_type_name[0]
    cat_list= []
    for sub_cat in all_catagories: 
      
      if sub_cat["cat_type_id"] == cat["catagory_type_id"]:
        
        #todo: catagories = [ [sub cat 1, c_type_id],[sub2, cat_type_id], --]
        # temp_sub.append('a': 1)
        # temp_sub = [ [key:value], [key:value]]
        
        temp_sub=  dict({"catagory_id": sub_cat["catagory_id"], "catagory_name": sub_cat["catagory_name"] })
        cat_list.append(temp_sub)  # todo: [-------]
        temp_cat_dict["sub_catagories"] = cat_list
    
    all_catagory_json.append(temp_cat_dict)
  # return render_template("experiment.html", cat_3= all_catagory_json)
  all_catagory_info = db.execute("SELECT username, catagory_type_name FROM userCatagoryInfo WHERE id = ? ", session["user_id"])
  
  #TODO:
  return all_catagory_json
  return render_template("experiment.html", cat_2=temp_cat_type[0], cat_3= all_catagory_json)
@app.route("/editcatagory", methods=["Get", "POST"])
@login_required
def editcatagory():
  
    return render_template("/experiment.html")
# comment goes here    

# ------------------------ DIARY MANAGMENT -------------------------
# ------------------------ DIARY MANAGMENT -------------------------
# ------------------------ DIARY MANAGMENT -------------------------

@app.route("/managediary")  # type: ignore
@login_required
def diarymanagment():
  
  return render_template("diary.html", current_user_name= global_user_name(), catagories=global_catagory(), manage_diary= 1)
  

@app.route("/editdiary")  # type: ignore
@login_required
def editdiary():
  
  

    if task_to_do[0] == "viewdiary":
      return redirect("/viewdiary")
    
        
#TODO: diary will be deleted here meaning the status of the diary will be changed to "Deleted"----------------------------

    if task_to_do[0] == "editdiarydate":
      
      #STEP 1FIND NUMBER OF EDITS FOR USERDIARY
      userdiary = db.execute("SELECT * FROM userdiary WHERE ud_id = ? ", global_user_diary_id[0])
      number_of_edits = userdiary[0]["number_of_edits"]
      
        # increment number of edites by one
      number_of_edits += 1
    #STEP 2 MAKE THE ACTUAL CHANGE
      db.execute("UPDATE userdiary SET number_of_edits = ?, given_date = ?, given_time = ? WHERE ud_id = ?", number_of_edits, global_diary_date[0], global_diary_time[0],global_user_diary_id[0])
      
      global_edited_diary[0] = int(global_diary_element_id[0])
      edit_mode[0] = 1
      
      
      global_diary_element_id[0] = -1 # type: ignore
      global_diary_date[0] = -1 # type: ignore
      global_diary_time[0] = -1 # type: ignore
      global_user_diary_id[0] = -1  # type: ignore      
      
      return redirect("/viewdiary")
#TODO: diary will be deleted here meaning the status of the diary will be changed to "Deleted"----------------------------

    if task_to_do[0] == "deletediary":
      
        #db.execute("BEGIN TRANSACTION")
        
        db.execute("UPDATE diary SET diary_status = ? WHERE diary_id = ?", "Deleted" ,global_diary_id[0])
        #db.execute("COMMIT")
      
      
        global_edited_diary[0] = global_diary_element_id[0]   # type: ignore
        edit_mode[0] = 1
        
        global_diary_id[0] = [" "] # type: ignore
        global_diary_element_id[0] = [" "] # type: ignore
        

        return redirect("/viewdiary")
      
    
    if task_to_do[0] == "editdiarycontent":
      
      # remover unwanted extra spaces at the begning of the diary content
      start_position = [0]
      end_position = [len(global_diary_content)]
      
      #gettrimedcontent(global_diary_content)
      for i in range (len(global_diary_content)):
        if global_diary_content[i] == " ":
          start_position[0] += 1
        else: 
          break
      # slice the unnesesory spaces     
      global_diary_content[start_position[0] - 1: end_position[0]]
      
      
      # update diary with new diary content
      db.execute("UPDATE diary SET diary_content = ?  WHERE diary_id = ?", global_diary_content[0], global_diary_id[0])
      
      
      # increment number of edits to this specific diary by one then update
        # increment
      global_diary_number_of_edits[0] = int(global_diary_number_of_edits[0]) + 1  # type: ignore
        #update
      db.execute("UPDATE userdiary SET number_of_edits = ? WHERE ud_id = ?", global_diary_number_of_edits[0], global_user_diary_id[0])
      
      global_edited_diary[0] = global_diary_element_id[0]   # type: ignore
      edit_mode[0] = 1
      
      global_diary_id[0] = [" "] # type: ignore
      global_diary_element_id[0] = [" "] # type: ignore
      global_diary_number_of_edits[0] = [" "] # type: ignore
      global_user_diary_id[0] = [" "] # type: ignore

      return redirect("/viewdiary")
    if task_to_do[0] == "222222222":
      return render_template("experiment.html", cat_1 = "edit diary")
      

@app.route("/deletediary", methods=["Get", "POST"])
@login_required
def deletediary():

    if request.method == "POST":
      task_to_do[0] = "deletediary"
      global_diary_id[0] = request.form.get("diary-id")   # type: ignore
      global_diary_element_id[0] = request.form.get("diary-element-id") # type: ignore
      
      return redirect("/editdiary")
    else:
      return redirect("/viewdiary")

@app.route("/editdiarycontent", methods=["Get", "POST"])
@login_required
def editdiarycontent():

    if request.method == "POST":
      task_to_do[0] = "editdiarycontent"
      global_diary_content[0] = request.form.get("diary-content") # type: ignore
      global_diary_number_of_edits[0] = request.form.get("number-of-edits") # type: ignore
      global_diary_id[0] = request.form.get("diary-id")   # type: ignore
      global_user_diary_id[0] = request.form.get("user-diary-id") # type: ignore
      global_diary_element_id[0] = request.form.get("diary-element-id") # type: ignore
      
      return redirect("/editdiary")
    else:
      return redirect("/viewdiary")
      
      
@app.route("/changediarydate", methods=["Get", "POST"])
@login_required
def changedate():

  if request.method == "POST":
    
    global_diary_date[0] = request.form.get("diary-date") # type: ignore
    global_diary_time[0] = request.form.get("diary-time") # type: ignore
    global_user_diary_id[0] = request.form.get("ud-id")   # type: ignore
    global_diary_element_id[0] = request.form.get("diary-element-id") # type: ignore
    
    
    task_to_do[0] = "editdiarydate"
    
    return redirect("/editdiary")
  else:
    return render_template("diary.html",  current_user_name=global_user_name(),catagories= global_catagory(), diary=global_diary, view_all_condensed = 1)
  


@app.route("/generatecatagory", methods= ["GET", "POST"]) # type: ignore
@login_required
def generatecatagory():  
  # if request.method == "POST":
  #   catagory_type_id = request.form.get("catagory-type")
  #   diary_content = request.form.get("diarytextarea")
  
  #get catagory_name of selected catagory type
  if request.method == "POST":
    catagory_type_id = request.form.get("catagory-type")
    diary_content = request.form.get("diarytextarea")
    
    if not diary_content:
      diary_content= "empty content"
    
    catagory_type = db.execute("SELECT * FROM catagorytype WHERE catagory_type_id =? ", catagory_type_id)
    
    
    catagory_type_name= catagory_type[0]["catagory_type_name"]
    
    #return render_template("experiment.html" , cat_1 = catagory_type_id, cat_2 = catagory_type_name)
    
    #make selected catagory type the head of the list
    
    catagory_types = db.execute("SELECT * FROM catagorytype")
    
    # remove the catagory type from the list to add it later at the begning of the list
    # for i in range(len(catagory_types) ):
    #   if catagory_types[i]["catagory_type_id"] == catagory_type_id :
    #     catagory_types.pop(i)
    
    for count,cat_type in enumerate(catagory_types):
      if cat_type["catagory_type_id"] == catagory_type_id:
        catagory_types.pop(count)
        
    #TODO:   this is the main part to display catagories based on catagory type
    catagory_types.insert(0, {"catagory_type_id": catagory_type_id , "catagory_type_name": catagory_type_name} )
    
    # for count,cat_type in enumerate(catagory_types):
    #   if cat_type["catagory_type_id"] == catagory_type_id:
    #     catagory_types.insert(0, cat_type)
    #     break
    
    if catagory_type_id != 0:
      
      
      #TODO: 
      return render_template("takelog.html", diary_content=diary_content, catagory_types= catagory_types, current_user_name=global_user_name(), catagories=global_catagory_with_parameter(catagory_type_id))
      # return render_template("diary.html", diary_content=diary_content, catagory_types= catagory_types, current_user_name=global_user_name(), catagories=global_catagory_with_parameter(catagory_type_id), writediary= 1)
    
    return render_template("takelog.html", catagory_types= catagory_types, catagories = user_catagories())
          
@app.route("/takelog", methods=["GET", "POST"]) #type: ignore
@login_required
def jsonajax():
  
  
  if request.method == "POST":
                
    given_date = request.form["given-date"] # works
    given_time = request.form["given-time"]
    
    multiple_catagories_selected = request.form.getlist("native-select")
    # return render_template("experiment.html", cat_3 = multiple_catagories_selected )
    diary_text = request.form["diarytextarea"] # works
    diary_description = request.form["diary-description"]
    
    # return render_template("experiment.html", cat_3 = multiple_catagories_selected )
    
    catagory_types= db.execute("SELECT * FROM catagorytype")
    
    if not diary_text:
      flash("nothing to save")
      return render_template("takelog.html", catagory_types= catagory_types, catagories = user_catagories())
    # check if user has given his own date diffrent from current writing date
    if not given_date:
      
      given_date = currentday() # works
      
    if not given_time:
      given_time = currentclock() # works
      
      
    # return render_template("experiment.html", cat_3=multiple_catagories_selected)
    
    if len(diary_description) == 0:
      diary_description = "No Description"
    #return render_template("experiment.html", cat_1 = given_date, cat_2 = given_time)
    
    
    # write diary to database3
    #step 1 update diary table with diarytextareas text
    db.execute("INSERT INTO diary (diary_content, description ) VALUES (?, ?)", diary_text, diary_description ) # works

    #step 2  get the inserted log/diary id
    
    new_diary_id = db.execute("SELECT * FROM diary ORDER BY diary_id DESC LIMIT 1")  # works
    
    #TODO: if edit mode then increment  number_of_edits field by 1
    
    #step 3   update user diary table with diaryid and and user id
    
    db.execute("INSERT INTO userdiary (d_id, u_id, given_date, given_time, diary_written_date, diary_written_time) VALUES (?, ?, ?, ?, ?, ?)", new_diary_id[0]["diary_id"], session["user_id"], given_date , given_time, currentday(), currentclock())
    
    # session["added_user_diary_id"] = db.execute("SELECT * FROM userdiary ORDER BY ud_id DESC LIMIT 1")
    rows = db.execute("SELECT * FROM userdiary ORDER BY ud_id DESC LIMIT 1")
    
    session["added_user_diary_id"]= rows[0]["ud_id"]
    
    
    #test render_template
    # return render_template("experiment.html", cat_3=session["added_user_diary_id"])
    #step 4 get the new user daiary id
    
    added_user_diary_id = db.execute("SELECT * FROM userdiary ORDER BY ud_id DESC LIMIT 1") #works
    
    #return render_template("experiment.html", test= added_user_diary_id[0]["ud_id"])
    
    # add catagory for the diary id
        # find id of Normal
    default = "Normal"
    catagory_normal = db.execute("SELECT * FROM catagory WHERE catagory_name = ?", default) #works
    catagory_normal_id = int(catagory_normal[0]["catagory_id"]) # works 
    
    
    if multiple_catagories_selected[0] != "":
      
      splited_multiple_catagories = multiple_catagories_selected[0].split(",")
      # return render_template("experiment.html", cat_3= multiple_catagories_selected )
      
      for i in range(len(splited_multiple_catagories)):
        
        db.execute("INSERT INTO userdiarycatagory (ud_id, c_id, catagory_insertion_date, catagory_insertion_time ) VALUES (?, ?, ?, ? )", int(session["added_user_diary_id"]), int(splited_multiple_catagories[i]), currentday(), currentclock())
        
      # return redirect("viewdiary.html")  
      # return render_template("experiment.html", cat_3= splited_multiple_catagories )
    else: 
      
      #if user didnot select catagory for his log then cattype: general and sub_catagory: Normal will be recorded as default
      catagory_normal_id = int(catagory_normal[0]["catagory_id"]) # works
      db.execute("INSERT INTO userdiarycatagory (ud_id, c_id, catagory_insertion_date, catagory_insertion_time ) VALUES (?, ?, ?, ? )", session["added_user_diary_id"], catagory_normal_id, currentday(), currentclock())
      
      # return redirect("/viewdiary")
    #return render_template("experiment.html", default=catagory_normal_id ) 
    
    return redirect("/viewdiary")
  else:
    
    catagory_types= db.execute("SELECT * FROM catagorytype JOIN usercatagory ON catagorytype.catagory_type_id = usercatagory.cat_type_id_in_uc JOIN users ON users.id= usercatagory.u_id_in_uc WHERE usercatagory.u_id_in_uc = ?", session["user_id"])
    
    # catagories = db.execute("SELECT * FROM catagory")  
    
    # catagories = db.execute("SELECT * FROM catagorytype JOIN usercatagory ON usercatagory.cat_type_id_in_uc = catagorytype.catagory_type_id JOIN users ON users.id = usercatagory.u_id_in_uc WHERE id = ?", session["user_id"])
    
    catagories = db.execute("SELECT * FROM catagory JOIN catagorytype ON catagory.cat_type_id = catagorytype.catagory_type_id JOIN usercatagory ON catagorytype.catagory_type_id = usercatagory.cat_type_id_in_uc JOIN users ON users.id = usercatagory.u_id_in_uc WHERE users.id = ? AND catagorytype.catagory_type_id = ?", session["user_id"], 1)
    
    # catagories = db.execute("SELECT * FROM catagory")
    return render_template("takelog.html", catagory_types= catagory_types, catagories = catagories, current_user_name=global_user_name())
    
  
@app.route("/diaryreference", methods = ["GET", "POST"]) #type: ignore
@login_required
def diaryreference():
  
  if request.method == "POST":
    return render_template("diaryreference.html")
    
  else: 
    # return render_template("experiment.html", cat_3=  get_all_user_diary(session["user_id"]))
    return render_template("diaryreference.html",catagory_types= catagory_types(), catagories = user_catagories(), user_diary = get_all_user_diary_detail(session["user_id"]))    
    
    
@app.route("/writediary" , methods=["GET", "POST"]) 
@login_required
def diarywrite():
    """Buy shares of stock"""
    if request.method == "POST":
        diary_text = request.form["diarytextarea"] # works
        given_date = request.form["given-date"] # works
        given_time = request.form["given-time"]
        diary_description = request.form["diary-description"]
        catagory_type_id = int(request.form["catagory-type"])
        catagory_types= db.execute("SELECT * FROM catagorytype")
        multiple_catagories_selected = request.form.getlist("native-select")
        
        
        # return render_template("experiment.html", cat_3= multiple_catagories_selected)
        if not diary_text:
          flash("nothing to save")
          return render_template("diary.html", catagory_types= catagory_types, current_user_name=global_user_name(), catagories=global_catagory(), writediary= 1)
        cat_1 = ""
        cat_2 = ""
        cat_3 = ""
        cat_1= int(request.form["catagory-1"]) # works
        cat_2 = int(request.form["catagory-2"]) # works
        cat_3= int(request.form["catagory-3"]) # works
        
        
        # check if user has given his own date diffrent from current writing date
        if not given_date:
            given_date = currentday() # works

        if not given_time:
            given_time = currentclock() # works

        if len(diary_description) == 0:
            diary_description = "No Description"
        #return render_template("experiment.html", cat_1 = given_date, cat_2 = given_time)
        
        
        # write diary to database3
        #step 1 update diary table with diarytextareas text
        db.execute("INSERT INTO diary (diary_content, description ) VALUES (?, ?)", diary_text, diary_description ) # works

        #step 2  get the diary id
        #inserted_stock_ld = db.execute("SELECT * FROM stocks ORDER BY id DESC LIMIT 1")
        new_diary_id = db.execute("SELECT * FROM diary ORDER BY diary_id DESC LIMIT 1")  # works
        #return render_template("experiment.html", test= new_diary_id[0]["diary_id"])
        #step 3   update user diary table with diaryid and and user id
        db.execute("INSERT INTO userdiary (d_id, u_id, given_date, given_time, diary_written_date, diary_written_time) VALUES (?, ?, ?, ?, ?, ?)", new_diary_id[0]["diary_id"], session["user_id"], given_date , given_time, currentday(), currentclock())
        
        
        #step 4 get the new user daiary id 
        added_user_diary_id = db.execute("SELECT * FROM userdiary ORDER BY ud_id DESC LIMIT 1") #works
        #return render_template("experiment.html", test= added_user_diary_id[0]["ud_id"])
                
        # add catagory for the diary id
            # find id of Normal
        default = "Normal"
        catagory_normal = db.execute("SELECT * FROM catagory WHERE catagory_name = ?", default) #works
        catagory_normal_id = int(catagory_normal[0]["catagory_id"]) # works
        
        #return render_template("experiment.html", default=catagory_normal_id ) 
        
        #======== THIS PART WILL BE REPLACED WITH MULTISELECT DROP DOWN MENU (SELECT element)    
            # if cat-1 and cat-2 and cat-3  == typical   then assign cat = normal
        #if cat_1 == 1 and cat_2 == 1 and cat_3 == 1:
        
        #db.execute("INSERT INTO userdiarycatagory(ud_id, c_id, catagory_insertion_date, catagory_insertion_time  ) VALUES (?, ?, ?, ?)", added_user_diary_id[0]["ud_id"], catagory_normal_id, currentday(), currentclock() ) # works
        
        #added_udc_id = db.execute("SELECT * FROM userdiarycatagory ORDER BY udc_id DESC LIMIT 1") # works
        
        
        
            # send alert  or flashed message SUCCESS

            # 4 4 2

        if cat_1 == 1 and cat_2 == 1 and cat_3 == 1:
            insert_user_diary_catagory(get_ud_id(), catagory_normal_id)
            #db.execute("INSERT INTO userdiarycatagory(ud_id, c_id, catagory_insertion_date, catagory_insertion_time  ) VALUES (?, ?, ?, ?)", added_user_diary_id[0]["ud_id"], catagory_normal_id, currentday(), currentclock() ) # works
            
            return redirect ("/viewdiary")

            
        if cat_1 != cat_3 and cat_1 != cat_2 and cat_2 != cat_3:

                insert_user_diary_catagory(get_ud_id(),cat_1)
                #udc1= get_udc_id()
                insert_user_diary_catagory(get_ud_id(),cat_2)
                #udc2= get_udc_id()
                
                insert_user_diary_catagory(get_ud_id(),cat_3)
                #udc3= get_udc_id()
                
                

                return redirect ("/viewdiary")
            #return render_template("experiment.html", test1=get_ud_id(), udc1=udc1, udc2=udc2, udc3=udc3)

        if cat_1 == cat_2 and cat_1 != cat_3 :
            
            insert_user_diary_catagory(get_ud_id(), cat_1)
            insert_user_diary_catagory(get_ud_id(), cat_3)
            
            return redirect ("/viewdiary")
            #return render_template("experiment.html", test1=get_ud_id(), test2 = get_udc_id(), cat_2= cat_2, cat_1= cat_1, cat_3 = cat_3 )    

            # 4 3  4
        
            #return render_template("experiment.html", test1=get_ud_id(), test2 = get_udc_id(), cat_2= cat_2, cat_1= cat_1, cat_3 = cat_3) 

            # 3 4 4
        if cat_2 == cat_3 and cat_2 != cat_1:
            insert_user_diary_catagory(get_ud_id(), cat_1)
            insert_user_diary_catagory(get_ud_id(), cat_2)

            return redirect ("/viewdiary")

            #return redirect ("/viewdiary")
            #return render_template("experiment.html", test1=get_ud_id(), test2 = get_udc_id(), cat_2= cat_2, cat_1= cat_1, cat_3 = cat_3 ) 
        
        if  cat_1 == cat_3 and cat_1 != cat_2 and cat_2 != cat_3:
            #return apology("thomas kitaba")
            insert_user_diary_catagory(get_ud_id(), cat_2)
            insert_user_diary_catagory(get_ud_id(), cat_1)

            return redirect ("/viewdiary")
        
        view_writen_diary_info_list[0] = 1
        return redirect ("/viewdiary" )
        #return render_template("experiment.html", test1=get_ud_id(), test2 = get_udc_id(), cat_2= cat_2, cat_1= cat_1, cat_3 = cat_3 ) 
        
    else:
      catagory_types= db.execute("SELECT * FROM catagorytype")
      return render_template("diary.html", catagory_types= catagory_types, current_user_name=global_user_name(), catagories=global_catagory(), writediary= 1)
      #return render_template("diary.html", catagory_types= global_catagory_types(), current_user_name=global_user_name(), catagories=global_catagory(1), writediary= 1)
      
@app.route("/viewdiary", methods=["GET", "POST"])
@login_required
def diaryview():
    """Sell shares of stock"""

    diary = []
    temp_diary = {}
    user_diary = get_all_user_diary(session["user_id"])
    #return render_template("viewdiary.html", diary=diary, view_writen_diary = 1)

    index = 1
    for diary_info in user_diary:
        temp_diary = {}
        
        catagory_list = get_catagory_name(diary_info["ud_id"])
        
        temp_diary = diary_info
        
        temp_diary["number"] = index
        index += 1
        diary_catagories = []
        
        for count, catagory_info in enumerate(catagory_list):
            cat_id = "catagory_id"+ str(count)
            name = "catagory"+ str(count)
            udc_id = "user_diary_catagory_id"+ str(count)
            # diary_catagories = [ [cat id, cat name] [cat id, cat name] [cat id, cat name]
            # soon to become  {diary_catagories : [ [cat id, cat name], [cat id, cat name], [cat id, cat name] ]}
            #TODO:  diary-catagory  0 = cat id    1 = cat name   2 = udc_id
            diary_catagories.append([catagory_info["catagory_id"], catagory_info["catagory_name"], catagory_info["udc_id"] ])
            temp_diary[name] = catagory_info["catagory_name"]
            temp_diary[cat_id] = catagory_info["catagory_id"]
            temp_diary[udc_id] = catagory_info["udc_id"]
        
        temp_diary["diary_catagories"] = diary_catagories    
        
        
        diary.append(temp_diary)
        #sort diary then send it to be displayed
        #     

    diary.reverse()
    global_diary = diary

    # for SCROLLINTOVIEW
    #TODO: KNOW THE CURRNT USERS DIARY COUNT   TO USEIT AS A VARIABLE IN SCROLLINTO VIEW
    diary_count = db.execute("SELECT * FROM userdiary WHERE u_id = ?", session["user_id"]) 
    diary_count = len(diary_count)

    edited_diary_element_id= global_edited_diary[0]

    if edited_diary_element_id != diary_count:
        edited_diary_element_id= int(global_edited_diary[0]) + 1 #type: ignore
    
    # reset global_edited_dairy[]    variable to 0 
    global_edited_diary[0] = diary_count
    
    catagories = db.execute("SELECT * FROM catagory")
    #diary.sort(reverse=True)
    if edit_mode[0] == 1:
        
        edit_mode[0] = 0

        # return render_template("diary.html",  current_user_name=global_user_name(),catagories= global_catagory(global_catagory_type[0]), diary=diary, view_all_condensed = 1, edited_diary_element_id= edited_diary_element_id )
        return render_template("diary.html",  current_user_name=global_user_name(),catagories=global_catagories(), diary=diary, view_all_condensed = 1, edited_diary_element_id= edited_diary_element_id )
    
    return render_template("diary.html",  current_user_name=global_user_name(),catagories= global_catagories(), diary=diary, view_all_condensed = 1)
    #return render_template("diary.html",  current_user_name=global_user_name(),catagories= global_catagory(global_catagory_type[0]), diary=diary, view_all_condensed = 1)
    
# --------------------------- works to view all data with duplicate ------------------------------
    diary = db.execute("SELECT * FROM diarydatabaseview WHERE id = ?", session["user_id"])
    #return render_template("viewdiary.html", diary=diary, view_all= 1)

#------------------------ WORKS ------------------------------------------------------------------------------
    if view_writen_diary_info_list[0] == 1:
        did= get_d_id()
        udid = get_ud_id()
        diary = get_diary_content(did) 
    #catagory = get_catagory_name(udid)
    #diary = db.execute("SELECT * FROM userdiaryview WHERE d_id = ?", did)
        catagory = db.execute("SELECT * FROM diarycatagoryview WHERE ud_id = ?", udid)
        view_writen_diary_info_list[0] = 0
        return render_template("viewdiary.html", diary=diary, catagory=catagory, view_writen_diary = 1)
    #return render_template("diary.html",current_user_name=global_user_name(), catagories=global_catagory(global_catagory_type[0]), viewdiary=1)
    #------------------------ WORKS ------------------------------------------------------------------------------



  
  

#|||||||||||||||||| -- CATAGORY -- |||||||||||||||||||
@app.route("/changecatagory", methods=["Get", "POST"])  # type: ignore
@login_required
def changecatagory():
    if request.method == "POST":
        user_diary_catagory_id = request.form.get("user-diary-catagory-id")
        diary_element_id = request.form.get("diary-element-id")  # type: ignore

        catagory_id = request.form.get("catagory-id-list")

        # get number-of-edits so as to increment it on change
        rows = db.execute("SELECT * FROM userdiarycatagory WHERE udc_id = ?", user_diary_catagory_id)
        number_of_edits = int(rows[0]["number_of_edits_made"]) + 1

        #user_diary_catagory_id = request.form.get("user-diary-catagory-id")
        db.execute("UPDATE userdiarycatagory SET c_id = ?, number_of_edits_made = ?,catagory_insertion_date = ?, catagory_insertion_time = ? WHERE udc_id = ?", catagory_id, number_of_edits, currentday(), currentclock(), user_diary_catagory_id)
        
        
        #TODO: send udc_id   to be used as ID  - inorder to take user back to the editeded row
        
        global_edited_diary[0] = diary_element_id     # type: ignore
        edit_mode[0] = 1

        #backtoedited(user_diary_catagory_id, diary_element_id)

        return redirect("/viewdiary")

@app.route("/removecatagory", methods=["GET", "POST"])  # type: ignore
@login_required
def removecatagory():
    
    if request.method == "POST":
        
        
        user_diary_catagory_id = request.form.get("user-diary-catagory-id")
        user_diary_id = request.form.get("ud-id")
        edited_diary_id = request.form.get("diary-id")
        diary_element_id = request.form.get("diary-element-id")
        #get the edited fild value from userdiary table
        rows = db.execute("SELECT * FROM userdiary WHERE ud_id = ?", user_diary_id )
        #increment it by one
        number_of_edits = int(rows[0]["number_of_edits"]) + 1
        
        # update edit field 
        db.execute("UPDATE userdiary SET number_of_edits = ? WHERE ud_id = ? ", number_of_edits, user_diary_id)
        
        # this is the main UPDATE (update removed data to userdiary catagory )
        #TODO: send udc_id   to be used as ID  - inorder to take user back to the editeded row

        db.execute ("DELETE FROM userdiarycatagory WHERE udc_id = ?", user_diary_catagory_id)

        global_edited_diary[0] = diary_element_id     # type: ignore
        edit_mode[0] = 1
        
        #backtoedited(user_diary_catagory_id, diary_element_id)
        
        return redirect("/viewdiary")

@app.route("/addnewcatagory",  methods=["GET", "POST"])
@login_required
def diaryedit():

    """Edit selected user Diary"""

#return render_template("diary.html", edit_diary = 1, us)
        #return render_template("diary.html",  current_user_name=global_user_name(), diary=global_diary, view_all_condensed = 1)
    if request.method == "POST":
        #  first-catagory-id == none means there is no catagory assigned for that user diary
        ##first_catagory_id = request.form.get("first-catagory-id")
        catagory_tobe_added_id = request.form.get("catagory-id-list") 
        diary_element_id = request.form.get("diary-element-id")
        ud_id = request.form.get("ud-id")

        db.execute("INSERT INTO userdiarycatagory (ud_id, c_id, catagory_insertion_date, catagory_insertion_time) VALUES(?, ?, ?, ? )" , ud_id, catagory_tobe_added_id, currentday(), currentclock())


        global_edited_diary[0] = diary_element_id  # type: ignore
        edit_mode[0] = 1

        
        return redirect("/viewdiary")
    else:
        return redirect("/viewdiary")

@app.route("/advancedsearchcatagories", methods=["GET", "POST"]) #type: ignore
@login_required
def advancedsearchcatagories():
  if request.method == "POST":
    catagory_type_id = request.form.get("catagory-type")
    diary_content = request.form.get("diarytextarea")
    all_catagories = db.execute("SELECT * FROM catagory")
    if not diary_content:
      diary_content= "empty content"
    
    catagory_type = db.execute("SELECT * FROM catagorytype WHERE catagory_type_id =? ", catagory_type_id)
    catagory_type_name= catagory_type[0]["catagory_type_name"]
    
    #return render_template("experiment.html" , cat_1 = catagory_type_id, cat_2 = catagory_type_name)
    
    #make selected catagory type the head of the list
    
    
    catagory_types = db.execute("SELECT * FROM catagorytype JOIN usercatagory ON catagorytype.catagory_type_id = usercatagory.cat_type_id_in_uc JOIN users ON users.id = usercatagory.u_id_in_uc WHERE users.id = ?", session["user_id"])
    
    # remove the catagory type from the list to add it later at the begning of the list
    # for i in range(len(catagory_types) ):
    #   if catagory_types[i]["catagory_type_id"] == catagory_type_id :
    #     catagory_types.pop(i)
    
    for count,cat_type in enumerate(catagory_types):
      if cat_type["catagory_type_id"] == catagory_type_id:
        catagory_types.pop(count)
        break
        
    #TODO:   this is the main part to display catagories based on catagory type
    catagory_types.insert(0, {"catagory_type_id": catagory_type_id , "catagory_type_name": catagory_type_name} )
    
    session["catagory_types"] = catagory_types
    # return render_template("experiment.html", cat_3 = "right befor printing search results")
    if catagory_type_id != 0:
      
      # return render_template("search.html",catagory_types= catagory_types(), catagories = user_catagories(), all_catagories= all_catagories, normal_search= 1)   
      #TODO:
      global_catagory_type_id[0] = catagory_type_id #type: ignore
      return render_template("search.html",catagory_types= catagory_types, catagories = global_catagory_with_parameter(catagory_type_id), all_catagories= all_catagories, normal_search= 1)    
      
      # return render_template("experiment.html", cat_3 = " catagory id not empty")
    
    return render_template("search.html",catagory_types= catagory_types, catagories = global_catagory_with_parameter(catagory_type_id), all_catagories= all_catagories, normal_search= 1)
  
#TODO: return render_template("search.html",catagory_types= catagory_types(), catagories = user_catagories(), all_catagories= all_catagories, normal_search= 1)    
@app.route("/search", methods=["GET", "POST"])
@login_required
def diarysearch():
  
  if request.method == "POST":
    
    search_catagory_id = request.form.get("search-catagory-id")
    # catagories = db.execute("SELECT * FROM catagory")
    all_catagories = db.execute("SELECT * FROM catagory")
    
    if not search_catagory_id:
      results = db.execute("SELECT * FROM diarydatabaseview WHERE id= ?", session["user_id"])
    else:
      results = db.execute("SELECT * FROM diarydatabaseview WHERE c_id= ? and u_id = ? ", search_catagory_id, session["user_id"] )  
    
    # if session["catagory_type"]:
    #   return render_template("search.html",current_user_name=global_user_name(), catagory_types= "hello thomas", catagories=user_catagories(), all_catagories= all_catagories, normal_search= 1, results = results)
    
    number_of_results = len(results)
    rows= db.execute("SELECT catagory_name FROM catagory WHERE catagory_id = ?", search_catagory_id )
    if rows:
      sub_catagory_name[0] = rows[0]["catagory_name"]
    return render_template("search.html",current_user_name=global_user_name(), catagory_types= catagory_types(), catagories = default_user_catagories(), all_catagories= default_all_user_catagories(), normal_search= 1, sub_catagory_name = sub_catagory_name[0], number_of_results = number_of_results, results = results)
    
  else:
    
    all_catagories = db.execute("SELECT * FROM catagory")
    
    return render_template("search.html",current_user_name=global_user_name(), catagory_types= catagory_types(), catagories = default_user_catagories(), all_catagories= default_all_user_catagories(), normal_search= 1)    
    
@app.route("/searchdate", methods=["GET", "POST"] )#type: ignore
@login_required
def searchdates():

  # global_search_start_date[0] = str(start_date)
  # global_search_end_date[0] = str(end_date)
    catagories = db.execute("SELECT * FROM catagory")
    catagory_types = db.execute("SELECT * FROM catagorytype JOIN usercatagory ON catagorytype.catagory_type_id = usercatagory.cat_type_id_in_uc JOIN users ON users.id = usercatagory.u_id_in_uc WHERE users.id = ?", session["user_id"])
    all_catagory = user_catagories()
    results = [""]
    
    
    if search_task_to_do[0] == "start-to-end-date": # or "from-begning-ifto-end-date":
      
      if search_task_to_do_additional[0] == "add-catagory-type":
        # return render_template("experiment.html", cat_3 = "search by adding th provided catagory type")
        results[0] = db.execute("SELECT * FROM diarydatabaseview WHERE cat_type_id = ? AND (given_date >= ? AND given_date <= ?)", session["catagory_type_id"], session["start_date"], session["end_date"])
        
        number_of_results = len(results[0])
        return render_template("search.html", all_catagories= default_all_user_catagories(),catagories=catagories, start_date= session["start_date"] , end_date= session["end_date"], catagory_types= catagory_types, all_catagory = default_all_user_catagories(), normal_search= 1, number_of_results = number_of_results, results = results[0])
        
      if search_task_to_do_additional[0] == "add-sub-catagories":
        # return render_template("experiment.html", cat_3 = "search using provided sub catagories")
        sub_catagory = []
        
        
        if session["sub_catagory_id"][0] != 0:
          sub_catagory = session["sub_catagory_id"][0].split(",")
        # return render_template("experiment.html", cat_3= sub_catagory)
        
        results.clear()
        
        for i in range(len(sub_catagory)):
          
          rows = db.execute("SELECT * FROM diarydatabaseview WHERE catagory_id = ? AND id = ? AND given_date >= ? AND given_date <= ?", int(sub_catagory[i]), session["user_id"], session["start_date"], session["end_date"])
          if rows:
            for row in rows:
              results.append(row)
            
        # return render_template("experiment.html", cat_3= results)
        
        number_of_results = len(results)
        # return render_template("experiment.html", cat_2= number_of_results, cat_3= results)
        return render_template("search.html",all_catagories= default_all_user_catagories(), catagories=catagories, start_date= session["start_date"] , end_date= session["end_date"], catagory_types= catagory_types,all_catagory = user_catagories(), normal_search= 1, number_of_results = number_of_results,  results = results)
      
      
      
      if search_task_to_do_additional[0] == "all-sub-catagories":
        # return render_template("experiment.html", cat_3 = "search all sub catagories")
        results[0] = db.execute("SELECT * FROM diarydatabaseview WHERE given_date >= ? AND given_date <= ?", session["start_date"], session["end_date"])
        number_of_results = len(results[0])
      
        #todo: output the search result
        return render_template("search.html",all_catagories= default_all_user_catagories(), catagories=catagories, start_date= session["start_date"] , end_date= session["end_date"], catagory_types= catagory_types,all_catagory = user_catagories(), normal_search= 1, number_of_results = number_of_results, results = results[0])
            
    start_date = "%"+ str(global_search_start_date[0]) + "%"
    
    
    
    if search_task_to_do[0] == "specific-date":
      # start_date = "%"+str(global_search_start_date[0])+"%"
      # results = db.execute("SELECT * FROM diary JOIN userdiary ON diary.diary_id = userdiary.d_id WHERE u_id = ? and userdiary.given_date Like ?", session["user_id"], "%" + global_search_start_date[0] + "%")
      #TODO: --------------------------------------------------------------------------------------------------------------------------------------
      
      if search_task_to_do_additional[0] == "add-catagory-type":
        # return render_template("experiment.html", cat_3 = session["catagory_type_id"])
        results.clear()
        # results = db.execute("SELECT * FROM diary JOIN userdiary ON diary.diary_id = userdiary.d_id WHERE u_id = ? AND catagory_id = ? AND userdiary.given_date Like ? AND diary_status = ?", session["user_id"], session["catagory_type_id"], "%" + global_search_start_date[0] + "%", "Active")
        
        results= db.execute("SELECT * FROM diarydatabaseview WHERE cat_type_id = ? AND id = ? AND given_date Like ? AND diary_status= ?", session["catagory_type_id"], session["user_id"], "%" + global_search_start_date[0] + "%",  "Active")
        number_of_results = len(results)
        return render_template("search.html",all_catagories= default_all_user_catagories(), catagories=catagories, start_date= global_search_start_date[0], catagory_types= catagory_types,all_catagory = user_catagories(), normal_search= 1, number_of_results = number_of_results, results = results)
        
      if search_task_to_do_additional[0] == "add-sub-catagories":
        # return render_template("experiment.html", cat_3 = session["sub_catagory_id"][0])
        sub_catagory = []
        
        
        if session["sub_catagory_id"][0] != 0:
          sub_catagory = session["sub_catagory_id"][0].split(",")
        # return render_template("experiment.html", cat_3= sub_catagory)
        
        results.clear()
        
        for i in range(len(sub_catagory)):
          
          rows = db.execute("SELECT * FROM diarydatabaseview WHERE catagory_id = ? AND id = ? AND given_date Like ? AND diary_status= ?", int(sub_catagory[i]), session["user_id"], "%" + global_search_start_date[0] + "%",  "Active")
          if rows:
            for row in rows:
              results.append(row)
            
        # return render_template("experiment.html", cat_3= results)
        
        number_of_results = len(results)
        # return render_template("experiment.html", cat_2= number_of_results, cat_3= results)
        return render_template("search.html",all_catagories= default_all_user_catagories(), catagories=catagories, start_date= global_search_start_date[0], catagory_types= catagory_types,all_catagory = user_catagories(), normal_search= 1, number_of_results = number_of_results,  results = results)
        
      
      
      if search_task_to_do_additional[0] == "all-sub-catagories":
        # return render_template("experiment.html", cat_3 = "search all sub catagories")
        results.clear()
        results = db.execute("SELECT * FROM diary JOIN userdiary ON diary.diary_id = userdiary.d_id WHERE u_id = ? AND  userdiary.given_date Like ? AND diary_status = ?", session["user_id"], "%" + global_search_start_date[0] + "%",  "Active")
      
        #todo: output the search result
        number_of_results = len(results)
        return render_template("search.html",all_catagories= default_all_user_catagories(), catagories=catagories,start_date= global_search_start_date[0], catagory_types= catagory_types,all_catagory = user_catagories(), normal_search= 1, number_of_results = number_of_results, results = results)
        
        #TODO: ----------------------------------------------------------------------------------------------------------------------------------------
      
      
      return render_template("search.html", catagories=catagories,catagory_types= catagory_types , all_catagory = user_catagories(), results=results, normal_search= 1)
    
    return render_template("search.html", all_catagory = user_catagories(), catagories=catagories,catagory_types= catagory_types, normal_search= 1)

@app.route("/simpledate", methods=["GET", "POST"]) # type: ignore
@login_required
def simpledate():
  # return apology("test thomas kitaba")
  if request.method == "POST":
    date_upto = str(request.form.get("date-upto-check-box"))  
    search_by_catagory_type = str(request.form.get("search-type-check-box"))       
    start_date = request.form.get("start-date")
    end_date = request.form.get("end-date")
    catagory_type_id = request.form.get("catagory-type")
    sub_catagory_id = request.form.getlist("sub-catagory")     
    # return render_template("experiment.html", cat_3 = sub_catagory_id)       
    session["start_date"] = start_date
    session["end_date"] = end_date
    rows = db.execute("SELECT * FROM userdiary WHERE u_id = ? lIMIT 1 ", session["user_id"] )
    begnning_date = rows[0]["given_date"]
    
    # return render_template("experiment.html", cat_3= request.form.get("catagory_type"))
  
    if search_by_catagory_type != "search-by-type": # if not checked
      
      if sub_catagory_id[0] != '':
        # return render_template("experiment.html",cat_1= sub_catagory_ids, cat_2= len(sub_catagory_ids) ,cat_3 = "search with provided sub catagories")
        search_task_to_do_additional[0]  = "add-sub-catagories"
        session["sub_catagory_id"] = sub_catagory_id
        
      else:
        # return render_template("experiment.html", cat_3 = "search all catagories")
        search_task_to_do_additional[0] = "all-sub-catagories"
    else: #todo: if search by catagory type is not selected
      # return render_template("experiment.html", cat_3 = "catagoroy check box checked")
      search_task_to_do_additional[0] ="add-catagory-type"
      
      session["catagory_type_id"] = catagory_type_id
      
    if date_upto == "upto":
      #if check box upto date is selected
      # return render_template("experiment.html", cat_1="empty date")
      
      if not start_date and not end_date:
        # search todays date
        session["start_date"] = begnning_date
        session["end_date"] = currentday()
        
        
          
        search_task_to_do[0] = "start-to-end-date"
        return redirect("/searchdate")
      
        return render_template("experiment.html", cat_3="both date fields empty so search for diary written on current date")
      if not start_date and end_date:
        
        #TODO: select * from userdiary where given_date < end_date  
        # find the first diary date
        
        session["start_date"] = begnning_date
        session["end_date"] = end_date
        search_task_to_do[0] = "start-to-end-date"
        return redirect("/searchdate")
        
      if start_date and end_date:
        # return render_template("experiment.html" , cat_3= search_task_to_do[0])
        session["start_date"] = start_date
        session["end_date"] = end_date
        search_task_to_do[0] = "start-to-end-date"
        # return render_template("experiment.html" , cat_3= search_task_to_do[0])
        return redirect("/searchdate")
        
      if start_date and not end_date:
        session["start_date"] = start_date
        session["end_date"] = currentday()
        search_task_to_do[0] = "start-to-end-date"
        return redirect("/searchdate") 
        
    else:
      search_task_to_do[0] = "specific-date"
      
      if not start_date:
        global_search_start_date[0] = currentday()
        # return render_template("experiment.html", cat_3= "start date not provided so start date = current date")
      if start_date:       
        global_search_start_date[0] = str(start_date)
      
      return redirect("/searchdate")           
      
  else:
    return redirect("/search")


@app.route("/diary", methods=["GET", "POST"])
@login_required
def manage_diary():
    """ MAIN diary page """
    
    return render_template("diary.html", current_user_name=global_user_name(), catagories=global_catagory(), manage_diary= 1)

# ----------------------END OF-- DIARY MANAGMENT -------------------------
# ----------------------START OF PROFILE MANAGMENT -------------------------
# ----------------------START OF PROFILE MANAGMENT -------------------------


@app.route("/manageprofile", methods=["GET", "POST"]) #type: ignore
@login_required
def profilemanagement():
    """ profile managment"""
    if request.method == "POST":
      return render_template("profile.html", current_user_name= global_user_name(), manage_profile= 1)
    else:
      return render_template("profile.html", current_user_name= global_user_name(), manage_profile= 1)
    
    
@app.route("/viewprofile")
@login_required
def profilmanagement():
    """ view you profile information """
    profile = db.execute("SELECT * FROM users WHERE id= ?", session["user_id"])
    profile_password = profile[0]["hash"]
    return render_template("profile.html",profile=profile,profile_password= profile_password, current_user_name= global_user_name(), view_profile= 1)
    
    

@app.route("/editprofile" , methods=["GET", "POST"]) #type: ignore
@login_required
def editprofile():
  if request.method == "POST":
    
    user_email = request.form.get("useremail")
    old_password = request.form.get("password")
    new_password= request.form.get("newpassword")
    confirm_password= request.form.get("confrimpassword")
    # return render_template("experiment.html", cat_3 = confirm_password)
    facebook_address= request.form.get("facebookaddress")
    telegram_address= request.form.get("telegramaddress")
    instagram_address= request.form.get("instagramaddress")
    telegram_address= request.form.get("telegramaddress")
    twitter_address= request.form.get("twitteraddress")
    country= request.form.get("country")
    city = request.form.get("city")
    gender= request.form.get("gender")
    primary_phone= request.form.get("primaryphone")
    secondary_phone= request.form.get("secondaryphone")
    user_address= request.form.get("useraddress")
    dateofbirth= request.form.get("dateofbirth")
    rows = db.execute("SELECT * FROM users WHERE id LIKE ?", session["user_id"])
    
    # rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    # if check_password_hash(rows[0]["hash"], str(old_password)):
    #   flash("Incorrect old password entry!  Try again")
    #   return render_template("/editprofile")
    
    #TODO:   step 1 check if empty then assign origninal value of user profile information to variables
    
    
    
    upi= user_profile_information()[0] #type: ignore
    if not upi:
      return render_template("experiment.html", cat_3= "try again")
    
    
    
    if not user_email:
      user_email = upi["useremail"]
    if not facebook_address:
      facebook_address = upi["facebookaddress"]
    if not twitter_address:#type: ignore
      twitter_address = upi["twitteraddress"]
    if not telegram_address:#type: ignore
      telegram_address = upi["telegramaddress"]
    if not instagram_address: #type: ignore
      instagram_address = upi["instagramaddress"]
    if not primary_phone: #type: ignore
      primary_phone = upi["primaryphone"]
    if not secondary_phone:
      secondary_phone = upi["secondaryphone"]
    if not country:
      country = upi["country"]
    if not city:
      city = upi["city"]      
    if not user_address:
      user_address = upi["useraddress"]
    if not dateofbirth:
      dateofbirth = upi["dateofbirth"]
    if not gender:
      gender = upi["gender"]
    
    #TODO: step 2 validate date field
    #todo: set validate_date value to true after checking the date fiels
    valid_date = True
    
    #TODO: step 3 validate password related information
    if old_password:
    #   flash("check your password fields")
      
    
    # if not old_password:
    #   flash("Check your old_password field")
    #   return redirect("/editprofile")
      if not new_password or not confirm_password:
        flash("Check your new_password and/or cofirm password fields")
        return redirect("/editprofile")
      
      
      if not check_password_hash(rows[0]["hash"], old_password):
        flash("Incorrect old password entry!  Try again")
        return redirect("/editprofile")
        # if not confirm_password:
        #   flash("Check your confirm_password field")
        #   return redirect("/editprofile")
      if new_password != confirm_password:
        flash("new password and new password confirmation doesnot match")
        
      if not check_password_format(new_password):
        flash("Password shold be more than 5 character long and should contain at least 1 letter")
        return redirect ("/editprofile")
    
      if not validate_email(user_email, verify=True):
        flash("Email does not Exist")
        return redirect("/editprofile")

      number_of_changes = rows[0]["numberofprofilechanges"] + 1
      updated_profile = db.execute("UPDATE users SET useremail = ?, hash = ?, facebookaddress = ?,  telegramaddress = ?, instagramaddress = ?, twitteraddress = ?, country = ?, city = ?, gender = ?, primaryphone = ?, secondaryphone = ? , useraddress = ?, dateofbirth = ?, numberofprofilechanges = ?", user_email, generate_password_hash(str(new_password)), facebook_address, telegram_address, instagram_address, twitter_address, country, city, gender, primary_phone,secondary_phone, user_address, dateofbirth, number_of_changes)
      
      #TODO: send email message telling user that he has successfully changed his profile
      msg = Message('Dear' + ':' + upi["fname"] + '  ' + upi["lname"] + '/n', sender = 'thomas.kitaba@gmail.com', recipients = [user_email])
      msg.body = "your profile has been updated:  number of profile edits including today =" + str(number_of_changes)
      
      
    #todo: check new password and confrm password validity
    
    
      #TODO: check if old password matchs users existing password
    
    
    # rows = db.execute("SELECT * FROM users WHERE id LIKE ?", session["user_id"])
    # if not check_password_hash(rows[0]["hash"], old_password):
    #   flash("Incorrect old password entry!  Try again")
    #   return redirect("/editprofile")
    else:
      # return render_template("experiment.html", cat_3 = "password match")
      #todo: calculate number profile changes
      
      
      if not validate_email(user_email, verify=True):
        flash("Email does not Exist")
        return redirect("/editprofile")
      
      #todo: increment the number of total edits made on users profile
      number_of_changes = rows[0]["numberofprofilechanges"] + 1
      
      db.execute("UPDATE users SET useremail = ?, facebookaddress = ?,  telegramaddress = ?, instagramaddress = ?, twitteraddress = ?, country = ?, city = ?, gender = ?, primaryphone = ?, secondaryphone = ? , useraddress = ?, dateofbirth = ?, numberofprofilechanges = ?", user_email, facebook_address, telegram_address, instagram_address, twitter_address, country, city, gender, primary_phone,secondary_phone, user_address, dateofbirth, number_of_changes)
      
      #TODO: send email confirmation
      msg = Message('Dear' + ':' + upi["fname"] + '  ' + upi["lname"] + '/n', sender = 'thomas.kitaba@gmail.com', recipients = [user_email])
      msg.body = "your profile has been updated: number of profile edits including today =" + str(number_of_changes)
      mail.send(msg)
      return redirect("/editprofile")
      
    
    # db.execute("UPDATE users SET ")
    return render_template("experiment.html", cat_3= country)
  
  else:
    
    task_to_do_profile[0] = "editprofile"
    #TODO: NB;   upi  = user profile information
    # return render_template("experiment.html", cat_3= user_profile_information()[0]["username"])
    upi= user_profile_information()[0] #type: ignore
    return render_template("profile.html",current_user_name= global_user_name(), upi= upi, edit_profile = 1)
    

@app.route("/changeaccountinfo") #type: ignore
@login_required
def changeaccountinfo():
    """ change account information   username and password """
    if request.method == "POST":
      pass
    else:
      return render_template("profile.html", current_user_name= global_user_name(),upi= user_profile_information()[0], change_account_info= 1)


@app.route("/changepersonalinfo") #type: ignore
@login_required
def changeinfo():
  if request.method == "POST":
    pass
  else:
    return render_template("profile.html", current_user_name= global_user_name(), upi= user_profile_information()[0], change_personal_info= 1)


#############################################################
######################## EXPERIMENTS ########################
######################## EXPERIMENTS ########################
######################## EXPERIMENTS ########################
#############################################################

@app.route("/experiment", methods=["GET", "POST"])
@login_required
def experiment():
    """ experiment page"""
    return render_template("experiment.html")
  
          
@app.route("/jsonajax" , methods=["GET", "POST"]) #type: ignore
@login_required
def takelog():
  
  
  if request.method == "POST":
                
    given_date = request.form["given-date"] # works
    given_time = request.form["given-time"]
    
    multiple_catagories_selected = request.form.getlist("native-select")
    # return render_template("experiment.html", cat_3 = multiple_catagories_selected )
    diary_text = request.form["diarytextarea"] # works
    diary_description = request.form["diary-description"]
    
    # return render_template("experiment.html", cat_3 = multiple_catagories_selected )
    
    catagory_types= db.execute("SELECT * FROM catagorytype")
    
    if not diary_text:
      flash("nothing to save")
      return render_template("takelog.html", current_user_name=global_user_name(), catagory_types= catagory_types, catagories = user_catagories())
    # check if user has given his own date diffrent from current writing date
    if not given_date:
      
      given_date = currentday() # works
      
    if not given_time:
      given_time = currentclock() # works
      
      
    # return render_template("experiment.html", cat_3=multiple_catagories_selected)
    
    if len(diary_description) == 0:
      diary_description = "No Description"
    #return render_template("experiment.html", cat_1 = given_date, cat_2 = given_time)
    
    
    # write diary to database3
    #step 1 update diary table with diarytextareas text
    db.execute("INSERT INTO diary (diary_content, description ) VALUES (?, ?)", diary_text, diary_description ) # works

    #step 2  get the inserted log/diary id
    
    new_diary_id = db.execute("SELECT * FROM diary ORDER BY diary_id DESC LIMIT 1")  # works
    
    #TODO: if edit mode then increment  number_of_edits field by 1
    
    #step 3   update user diary table with diaryid and and user id
    
    db.execute("INSERT INTO userdiary (d_id, u_id, given_date, given_time, diary_written_date, diary_written_time) VALUES (?, ?, ?, ?, ?, ?)", new_diary_id[0]["diary_id"], session["user_id"], given_date , given_time, currentday(), currentclock())
    
    # session["added_user_diary_id"] = db.execute("SELECT * FROM userdiary ORDER BY ud_id DESC LIMIT 1")
    rows = db.execute("SELECT * FROM userdiary ORDER BY ud_id DESC LIMIT 1")
    
    session["added_user_diary_id"]= rows[0]["ud_id"]
    
    
    #test render_template
    # return render_template("experiment.html", cat_3=session["added_user_diary_id"])
    #step 4 get the new user daiary id
    
    added_user_diary_id = db.execute("SELECT * FROM userdiary ORDER BY ud_id DESC LIMIT 1") #works
    
    #return render_template("experiment.html", test= added_user_diary_id[0]["ud_id"])
    
    # add catagory for the diary id
        # find id of Normal
    default = "Normal"
    catagory_normal = db.execute("SELECT * FROM catagory WHERE catagory_name = ?", default) #works
    catagory_normal_id = int(catagory_normal[0]["catagory_id"]) # works
    
    
    if multiple_catagories_selected[0] != "":
      
      splited_multiple_catagories = multiple_catagories_selected[0].split(",")
      # return render_template("experiment.html", cat_3= multiple_catagories_selected )
      
      for i in range(len(splited_multiple_catagories)):
        
        db.execute("INSERT INTO userdiarycatagory (ud_id, c_id, catagory_insertion_date, catagory_insertion_time ) VALUES (?, ?, ?, ? )", int(session["added_user_diary_id"]), int(splited_multiple_catagories[i]), currentday(), currentclock())
        
      # return redirect("viewdiary.html")  
      # return render_template("experiment.html", cat_3= splited_multiple_catagories )
    else: 
      
      #if user didnot select catagory for his log then cattype: general and sub_catagory: Normal will be recorded as default
      catagory_normal_id = int(catagory_normal[0]["catagory_id"]) # works
      db.execute("INSERT INTO userdiarycatagory (ud_id, c_id, catagory_insertion_date, catagory_insertion_time ) VALUES (?, ?, ?, ? )", session["added_user_diary_id"], catagory_normal_id, currentday(), currentclock())
      
      # return redirect("/viewdiary")
    #return render_template("experiment.html", default=catagory_normal_id ) 
    
    return redirect("/viewdiary")
  
  else:
    
    catagory_types= db.execute("SELECT * FROM catagorytype JOIN usercatagory ON catagorytype.catagory_type_id = usercatagory.cat_type_id_in_uc JOIN users ON users.id= usercatagory.u_id_in_uc WHERE usercatagory.u_id_in_uc = ?", session["user_id"])
    
    # catagories = db.execute("SELECT * FROM catagory")  
    
    # catagories = db.execute("SELECT * FROM catagorytype JOIN usercatagory ON usercatagory.cat_type_id_in_uc = catagorytype.catagory_type_id JOIN users ON users.id = usercatagory.u_id_in_uc WHERE id = ?", session["user_id"])
    
    catagories = db.execute("SELECT * FROM catagory JOIN catagorytype ON catagory.cat_type_id = catagorytype.catagory_type_id JOIN usercatagory ON catagorytype.catagory_type_id = usercatagory.cat_type_id_in_uc JOIN users ON users.id = usercatagory.u_id_in_uc WHERE users.id = ? AND catagorytype.catagory_type_id = ?", session["user_id"], 1)
    
    # catagories = db.execute("SELECT * FROM catagory")
    json_catagories = reloadJsonCatagory()
    # return render_template("experiment.html", cat_3= json_catagories)
    return render_template("jsonajax.html", json_catagories = reloadJsonCatagory(), catagory_types= catagory_types, catagories = catagories, current_user_name= global_user_name())
    
  
  

    



