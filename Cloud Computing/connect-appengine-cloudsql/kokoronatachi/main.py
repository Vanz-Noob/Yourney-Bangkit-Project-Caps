from crypt import methods
from lib2to3.pgen2 import token
import re
import os
import uuid
import pymysql
# from passlib.hash import sha256_crypt
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy, func
from functools import wraps
import jwt
import datetime
from db import get_destinasi, get_kategori, post_destinasi, post_kategori, get_db

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')
key = os.environ.get('SECRET')
sqlconn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(db_user, db_password, db_connection_name, db_name)

# cek API
app = Flask(__name__)

app.config['SECRET_KEY'] = key
app.config['SQLALHCEMY_DATABASE_URI'] = sqlconn
db = SQLAlchemy(app)

class user(db.Model):
    id_user = db.column(db.Interger(100), primary_key=True)
    id_public = db.column(db.String(100))
    username = db.column(db.String(100))
    password = db.column(db.String(100))

def username_exist(username):
    user = user.query.filter(func.lower(user.username) == func.lower(username)).first()
    return user

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = user.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/', methods=['GET'])
def hello():
    return jsonify({"message" : "hello world"})

# get DB
@app.route('/db', methods=['GET'])
@token_required
def get_user():
    return get_db()

# cek DB destinasi
@app.route('/destinasi', methods=['GET'])
def destinasi():
    return get_destinasi()

# tambah destinasi ke DB
@app.route('/addDest', methods=['POST'])
def add_destinasi():
    if not request.is_json:
        return jsonify({"Message": "Missing JSON"}), 400
    post_destinasi(request.get_json())
    return jsonify ({"Message" : "Destinasi berhasil ditambahkan"}), 200

# cek kategori DB
@app.route('/kategori', methods=['GET'])
def kategori():
    return get_kategori()

# tambah kategori ke DB
@app.route('/addKate', methods=['POST'])
def add_kategori():
    if not request.is_json:
        return jsonify({"Message": "Missing JSON"}), 400
    post_kategori(request.get_json())
    return jsonify ({"Message" : "Kategori berhasil ditambahkan"}), 200


@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = user.query.filter_by(name=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

@app.route('/register', methods=['POST'])
@token_required
def create_user(current_user):
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    data = request.get_json()

    exist = username_exist(data['name'])
    
    if not re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', data['password']):
        return jsonify({'message': 'password character must be atleast 8 character with capital case and number charachter'})
    
    if exist:
        return jsonify({'message': 'user already exist with this username'})

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = user(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=True)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message' : 'New user created!'})
# #login
# @app.route("/login",methods=["POST", "GET"])
# def login():
#     request_data = request.get_json()
#     username = request_data['username']
#     password = request_data['password']
#     Hpassword = sha256_crypt.encrypt(password)
#     #connect database
#     if os.environ.get('GAE_ENV') == 'standard':
#         unix_socket = '/cloudsql/{}'.format(db_connection_name)
#         cnx = pymysql.connect(user=db_user, password=db_password,
#                               unix_socket=unix_socket, db=db_name)

#     #querying sql
#     with cnx.cursor() as cursor:
#         cursor.execute('SELECT * FROM user WHERE username = %s', (username, ))
#         user = cursor.fetchone()
#     cnx.close()
#     if len(user) > 0:
#         if sha256_crypt.verify(password, user[2]):
#             return jsonify({'status': 'success', 'idUser': user[0], 'username': user[1]})
#         else:
#             return jsonify({'status': 'failed', 'message': 'Wrong password'})
#     else:
#         return jsonify({'status': 'failed', 'message': 'Wrong username'})
 
# #register
# @app.route("/register",methods=["POST", "GET"])
# def register():
#     request_data = request.get_json()
#     username = request_data['username']
#     password = request_data['password']
#     Hpassword = sha256_crypt.encrypt(password)   
    
#     #connect database
#     if os.environ.get('GAE_ENV') == 'standard':
#         unix_socket = '/cloudsql/{}'.format(db_connection_name)
#         cnx = pymysql.connect(user=db_user, password=db_password,
#                               unix_socket=unix_socket, db=db_name)
#     else:
#         host = '127.0.0.1'
#         cnx = pymysql.connect(user=db_user, password=db_password,
#                               host=host, db=db_name)
#     #querying sql
#     with cnx.cursor() as cursor:
#         cursor.execute('INSERT INTO user (username, password) VALUES (%s, %s);', (username, Hpassword))
#         result = cursor.fetchone()
#         cnx.commit()
#     cnx.close()
    
#     if result == 0:
#         js = {
#             "code": "gagal",
#         }
#     else:
#         js = {
#             "username": username,
#             "password": Hpassword,
#             "code": "sukses",
#         }
#     return jsonify(js)
    
    
     
if __name__ == '__main__':
    app.run()