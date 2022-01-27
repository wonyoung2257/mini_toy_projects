from flask import Flask, render_template, request, url_for, redirect, session
import pymongo
import bcrypt
#set app as a Flask instance 
app = Flask(__name__)
#encryption relies on secret keys so they could be run
app.secret_key = "testing"
#connoct to your Mongo DB database
client = pymongo.MongoClient('localhost', 27017)

#get the database name
db = client.get_database('dbjungle')
#get the particular collection that contains the data
records = db.register

#assign URLs to have a particular route 
@app.route("/", methods=['post', 'get'])
def index():
    message = ''
    #if method post in index
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        user = request.form.get("fullname")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        #if found in database showcase that it's found 
        user_found = records.find_one({"name": user})
        email_found = records.find_one({"email": email})
        if user_found:
            message = '사용하는 이름입니디.'
            return render_template('index.html.j2', message=message)
        if email_found:
            message = '이미 존재하는 이메일 입니다.'
            return render_template('index.html.j2', message=message)
        if password1 != password2:
            message = '비밀번호가 일치하지 않습니다.'
            return render_template('index.html.j2', message=message)
        else:
            #hash the password and encode it
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            #assing them in a dictionary in key value pairs
            user_input = {'name': user, 'email': email, 'password': hashed}
            #insert it in the record collection
            records.insert_one(user_input)
            
            #find the new created account and its email
            user_data = records.find_one({"email": email})
            new_email = user_data['email']
            #if registered redirect to logged in as the registered user
            return render_template('logged_in.html.j2', email=new_email)
    return render_template('index.html.j2')

@app.route("/login", methods=["POST", "GET"])
def login():
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("logged_in"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        #check if email exists in database
        email_found = records.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            #encode the password and check if it matches
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for('logged_in'))
            else:
                if "email" in session:
                    return redirect(url_for("logged_in"))
                message = '비밀번호 틀림!'
                return render_template('login.html.j2', message=message)
        else:
            message = '이메일을 찾을 수 없음'
            return render_template('login.html.j2', message=message)
    return render_template('login.html.j2', message=message)

@app.route('/logged_in')
def logged_in():
    if "email" in session:
        email = session["email"]
        return render_template('logged_in.html.j2', email=email)
    else:
        return redirect(url_for("login"))

@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return render_template("signout.html.j2")
    else:
        return render_template('index.html.j2')


if __name__ == "__main__":
  app.run(debug=True)
