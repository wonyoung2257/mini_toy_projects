from datetime import timedelta
from distutils.debug import DEBUG
from sre_constants import SUCCESS
from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_jwt_extended import *
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config.update(
  DEBUG = True,
  JWT_SECRET_KEY = 'SUPER KEY',
  JWT_TOKEN_LOCATION = 'cookies',
  JWT_ACCESS_TOKEN_RXPIRES = timedelta(hours = 1)
)

jwt = JWTManager(app)
from bson.objectid import ObjectId
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbCRUD

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/main')
@jwt_required(optional=True)
def main():
  current_identity = get_jwt_identity()
  if current_identity:
    borads = list(db.borad.find())
    print(borads)
    return render_template('main.html', borads = borads)
      # return redirect(url_for('main'))
  else:
    return redirect(url_for('home'))

@app.route('/login', methods = ['POST'])
def login():
  userId = request.form.get('id')
  userPW = request.form.get('pw')
  dbUser = db.user.find_one({'userId': userId})
  checkPW = bcrypt.check_password_hash(dbUser['password'], userPW)
  
  if(not dbUser):
    return jsonify({'result': 'fail', 'msg': '존재하지 않는 아이디 입니다.'})
  if(not checkPW):
    return jsonify({{'result': 'fail', 'msg': '비밀번호가 일치하지 않습니다..'}})
  if(dbUser and checkPW):
    access_token = create_access_token(identity=userId , expires_delta=False)
    resp = jsonify({'login': True})
    set_access_cookies(resp, access_token)
    return resp, 200
  else:
    return jsonify(result = 'Fail')

@app.route('/singup', methods = ['GET', 'POST'])
def singup():
  if request.method =='POST':
    id = request.form.get('id')
    pw = request.form.get('pw')
    if(db.user.find_one({'userId': id})): #아이디 이미 있을 때
      return jsonify({'result': 'exist', 'msg':'아이디가 이미 있음'})
    
    pw_hash = bcrypt.generate_password_hash(pw)
    doc = {'userId': id, 'password': pw_hash}
    db.user.insert_one(doc)
    return jsonify({'result': 'success', 'msg': '회원가입 되었습니다.'})
    
  else:
    return render_template('singup.html')

@app.route('/logout')
def logout():
  print('logout')
  resp = jsonify({'login': False})
  unset_access_cookies(resp)
  return resp


@app.route('/borad', methods = ['GET'])
@jwt_required(optional=True)
def borad():
  current_identity = get_jwt_identity()
  if current_identity :
    return render_template('boradWrite.html')
  else:
    return redirect(url_for('home'))
    

@app.route('/write', methods = ['POST'])
def write():
  # 글 작성 api
  title = request.form.get('title')
  contents = request.form.get('contents')
  userID = request.form.get('id')
  
  doc = {
    'title' : title,
    'contents' : contents,
    'userID' : userID,
  }
  db.borad.insert_one(doc)
  return jsonify({'result': 'success'})

@app.route('/detail', methods = ['GET'])
def detail():
  boradID = request.args.get('id')
  print(boradID)
  borad = db.borad.find_one({'_id':ObjectId(boradID)})
  print(borad)
  return render_template('borad.html', borad=borad )

if __name__ == '__main__':
  app.run('0.0.0.0', port=5000, debug =True)