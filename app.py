from flask import Flask, render_template, redirect, request, url_for, session, flash
import os
import pymongo
import bcrypt
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "testing"

picFolder = os.path.join('static','images')
app.config['UPLOAD_FOLDER'] = picFolder
favicon = os.path.join(app.config['UPLOAD_FOLDER'], 'favicon.ico')
style = os.path.join(app.config['UPLOAD_FOLDER'], '../style.css')

client = pymongo.MongoClient("mongodb+srv://N0L1F3R:Qwe12345@cluster0.9ye0c.mongodb.net/test")
db = client.get_database('homework2')
records = db.users

@app.route("/", methods=['post', 'get'])
def index():
  message = 'Please login to your account'

  if request.method == "POST":
    user = request.form.get("userName")
    password = request.form.get("password")

    user_found = records.find_one({"userName": user})
    if user_found:
      user_val = user_found['userName']
      passwordcheck = user_found['password']
            
      if check_password_hash(passwordcheck, password) is True:
        session["userName"] = user_val
        return redirect("/profile")
      else:
        if "userName" in session:
          return redirect("/profile")
        message = 'Wrong password ' + password + ' ' + hashedPassword
        return render_template('index.html', message=message, fav = favicon, styleCss = style)
    else:
      message = 'user not found'
      return render_template('index.html', message=message, fav = favicon, styleCss = style)
  return render_template("index.html", fav = favicon, styleCss = style)


@app.route("/register", methods=['post', 'get'])
def redirectToProfile():
  message = ''
  if request.method == "POST":
    user = request.form.get("userName")
        
    password1 = request.form.get("password1")
    password2 = request.form.get("password2")
        
    user_found = records.find_one({"userName": user})

    if user_found:
      message = 'There already is a user by that name'
      return render_template('register.html', message=message, fav = favicon, styleCss = style)
    if password1 != password2:
      message = 'Passwords should match!'
      return render_template('register.html', message=message, fav = favicon, styleCss = style)
    else:
      hashedPassword = generate_password_hash(password2)
      user_input = {'userName': user, 'password': hashedPassword}
      records.insert_one(user_input)
      return redirect("/")
  return render_template("register.html", fav = favicon, styleCss = style)

@app.route("/profile")
def profilePage():
  if session.get('userName') is None:
    return redirect("/")
  return render_template("profile.html", fav = favicon, styleCss = style)

@app.route("/settings", methods=['post', 'get'])
def updateProfile():
  if session.get('userName') is None:
    return redirect("/")

#   if request.method == "POST":
#     newUserName = request.form.get("newUserName")
#     password = request.form.get("password")
#     newPassword = request.form.get("newPassword")
#     oldName = session.get('userName')

#     user_found = records.find_one({"userName": oldName})
#     if user_found:
#       user_val = user_found['userName']
#       passwordcheck = user_found['password']
            
#       if newUserName is None:
#       if newPassword:
#         hashedPassword = generate_password_hash(newPassword)
#         user_input = {'userName': oldName, 'password': hashedPassword}
#         records.
#         message = 'Wrong password '
#         return render_template('index.html', message=message, fav = favicon, styleCss = style)
#     else:
#       message = 'user not found'
#       return render_template('index.html', message=message, fav = favicon, styleCss = style)
  return render_template("settings.html", fav = favicon, styleCss = style)

@app.route('/logout')
def logout():
  if session.get('userName') is None:
   return redirect("/")
  if session.get('userName'):
    del session['userName']
    flash('You have successfully logged yourself out.')
  return redirect('/')


if __name__ == "__main__":
  app.run(host="localhost", port=5000)