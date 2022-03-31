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
dbHW3 = client.get_database('homework3')

records = db.users
recordsPosts = dbHW3.posts
recordsSecretsPosts = dbHW3.secretPosts

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
        return render_template("profile.html", fav = favicon, styleCss = style)
      else:
        if "userName" in session:
          return render_template("profile.html", fav = favicon, styleCss = style)
        message = 'Wrong password '
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
  return render_template("register.html", message = message, fav = favicon, styleCss = style)

@app.route("/profile", methods=['post', 'get'])
def profilePage():
  message = ''
  if session.get('userName') is None:
    message = 'Log in to proceed'
    return render_template("index.html", message = message, fav = favicon, styleCss = style)
  return render_template("profile.html", fav = favicon, styleCss = style)

@app.route("/settings", methods=['post', 'get'])
def updateProfile():
  if session.get('userName') is None:
    return redirect("/")
  return render_template("settings.html", fav = favicon, styleCss = style)

@app.route('/logout')
def logout():
  if session.get('userName') is None:
   return redirect("/")
  if session.get('userName'):
    del session['userName']
    flash('You have successfully logged yourself out.')
  return redirect('/')

@app.route('/story')
def story():
  message = ''
  content = dbHW3.posts.find()
  secretContent = dbHW3.secretPosts.find()

  if session.get('userName') is None:
    message = 'null'

  return render_template("story.html", secretContent = secretContent, content = content, 
    fav = favicon, message = message, styleCss = style)

@app.route('/newStory', methods=['post', 'get'])
def newStory():
  message = ''
  if session.get('userName') is None:
    message = 'Register to write a post'
    return render_template("index.html", message = message, fav = favicon, styleCss = style)

  if request.method == "POST":
    author = session.get('userName')
    title = request.form.get("title")
    text = request.form.get("text")
    visibility = request.form.get("visibility")
    blog_post = {'author': author, 'title': title, 'text': text, 'visibility': visibility}

    if visibility == 'private':
      recordsSecretsPosts.insert_one(blog_post)
    else:
      recordsPosts.insert_one(blog_post)
    
    message = 'The post was successfully created!'

    return render_template("newStory.html", message = message, fav = favicon, styleCss = style)

  return render_template("newStory.html", message = message, fav = favicon, styleCss = style)


if __name__ == "__main__":
  app.run(host="localhost", port=5000)