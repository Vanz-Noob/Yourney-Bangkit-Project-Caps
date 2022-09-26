# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python38_cloudsql_mysql]
# [START gae_python3_cloudsql_mysql]
from crypt import methods
from hashlib import algorithms_available
from lib2to3.pgen2 import token
import os
from flask import Flask, jsonify, request, make_response
import pymysql
from passlib.hash import sha256_crypt
import re
from functools import wraps
import jwt
from datetime import datetime

# global resources
db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')
secret = os.environ.get('SEKRIT')

app = Flask(__name__)

def token_req(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        # parsing token pada endpoint
        token = request.args.get('token')
        # pengecekan token
        if not token:
            return make_response (
                jsonify({
                    "msg":"token not found",
                }), 404 
            )
        try:
            output = jwt.decode(token, secret, algorithms=["HS256"])
        except:
            return make_response (
                jsonify({
                    "msg": "invalid token"
                }), 500
            )
        return f(*args, **kwargs)
    return decorator

@app.route('/', methods=["GET"])
def hello():
    return "Hello, World This Is Yourney!"

#get all destinasi
@app.route('/destinasi')
def destinasi():
    destinasi = []
    if request.method == 'GET':
        if os.environ.get('GAE_ENV') == 'standard':
            # If deployed, use the local socket interface for accessing Cloud SQL
            unix_socket = '/cloudsql/{}'.format(db_connection_name)
            cnx = pymysql.connect(user=db_user, password=db_password,
                                unix_socket=unix_socket, db=db_name)
        with cnx.cursor() as cursor:
            cursor.execute('SELECT * FROM destinasi;')
            for row in cursor:
                destinasi.append({'id_destinasi': row[0], 'nama_destinasi': row[2], 'deskripsi': row[3]})
            cnx.close()
        return jsonify(destinasi)
    else:
        return 'Invalid request'  
       
#get all kategori
@app.route('/kategori')
def kategori():
    kategori = []
    if request.method == 'GET':
        if os.environ.get('GAE_ENV') == 'standard':
            # If deployed, use the local socket interface for accessing Cloud SQL
            unix_socket = '/cloudsql/{}'.format(db_connection_name)
            cnx = pymysql.connect(user=db_user, password=db_password,
                                unix_socket=unix_socket, db=db_name)
        with cnx.cursor() as cursor:
            cursor.execute('SELECT * FROM kategori;')
            for row in cursor:
                kategori.append({'id_kategori': row[0], 'nama_kategori': row[1]})
            cnx.close()
        return jsonify(kategori)
    else:
        return 'Invalid request'

#get all db
@app.route('/db')
@token_req
def db():
    #sudah okay
    users = []
    if request.method == 'GET':
        if os.environ.get('GAE_ENV') == 'standard':
            # If deployed, use the local socket interface for accessing Cloud SQL
            unix_socket = '/cloudsql/{}'.format(db_connection_name)
            cnx = pymysql.connect(user=db_user, password=db_password,
                                unix_socket=unix_socket, db=db_name)
        with cnx.cursor() as cursor:
            cursor.execute('SELECT * FROM user;')
            for row in cursor:
                users.append({'idUser': row[0], 'username': row[1], 'password': row[2]})
            cnx.close()
        return jsonify(users)
    else:
        return jsonify(
            {
                "msg": "login not found"
            }, 500
        )
       
    
#login
@app.route('/login',methods=["POST", "GET"])
def login():
    request_data = request.get_json()
    username = request_data['username']
    password = request_data['password']
    Hpassword = sha256_crypt.encrypt(password)
    #connect database
    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)

    #querying sql
    with cnx.cursor() as cursor:
        cursor.execute('SELECT * FROM user WHERE username = %s', (username, ))
        user = cursor.fetchone()
    cnx.close()
    # cek username dengan pass
    if len(user) > 0:
        if sha256_crypt.verify(password, user[2]):
            token = jwt.encode(
                {
                    "username":user[2],
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
                }, secret, algorithm="HS256"
            )
            return jsonify(
                {'status': 'success', 
                 'idUser': user[0], 
                 'username': user[1]}, 200
                )
        else:
            return jsonify(
                {'status': 'failed', 
                 'message': 'Wrong password'}, 400
                )
    else:
        return jsonify(
            {'status': 'failed',
             'message': 'Wrong username'}, 400
            )
 
#register
@app.route('/register',methods=["POST", "GET"])
def register():
    request_data = request.get_json()
    username = request_data['username']
    password = request_data['password']
    Hpassword = sha256_crypt.encrypt(password)   
    
    #connect database
    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    else:
        host = '127.0.0.1'
        cnx = pymysql.connect(user=db_user, password=db_password,
                              host=host, db=db_name)
    #querying sql
    with cnx.cursor() as cursor:
        cursor.execute('INSERT INTO user (username, password) VALUES (%s, %s);', (username, Hpassword))
        result = cursor.fetchone()
        cnx.commit()
    cnx.close()
    
    if result == 0:
        js = {
            "code": "gagal",
        }, 400
    else:
        token = jwt.encode(
            {
                "username":username,
                "password":Hpassword,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
            }, secret, algorithm="HS256"
        )
        js = {
            "username": username,
            "code": "sukses",
        }, 200
    return jsonify(js)

#add destinasi
@app.route('/addDest',methods=["POST", "GET"])
def addDestinasi():
    request_data = request.get_json()
    nama_destinasi = request_data['nama_destinasi']
    deskripsi = request_data['deskripsi']
   
    #connect database
    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    else:
        host = '127.0.0.1'
        cnx = pymysql.connect(user=db_user, password=db_password,
                              host=host, db=db_name)
    #querying sql
    with cnx.cursor() as cursor:
        cursor.execute('INSERT INTO destinasi (nama_destinasi, deskripsi) VALUES (%s, %s);', (nama_destinasi, deskripsi))
        result = cursor.fetchone()
        cnx.commit()
    cnx.close()
    
    if result == 0:
        js = {
            "code": "gagal",
        }, 400
    else:
        js = {
            "nama_destinasi": nama_destinasi,
            "deskripsi": deskripsi,
            "code": "sukses",
        }, 200
    return jsonify(js)

#add kategori
@app.route('/addKate',methods=["POST", "GET"])
def addKategori():
    request_data = request.get_json()
    nama_kategori = request_data['nama_kategori']
   
    #connect database
    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    else:
        host = '127.0.0.1'
        cnx = pymysql.connect(user=db_user, password=db_password,
                              host=host, db=db_name)
    #querying sql
    with cnx.cursor() as cursor:
        cursor.execute('INSERT INTO kategori (nama_kategori) VALUES (%s);', (nama_kategori))
        result = cursor.fetchone()
        cnx.commit()
    cnx.close()
    
    if result == 0:
        js = {
            "code": "gagal",
        }, 400
    else:
        js = {
            "nama_kategori": nama_kategori,
            "code": "sukses",
        }, 200
    return jsonify(js)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
