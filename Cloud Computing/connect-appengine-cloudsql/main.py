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
import os
from flask import Flask, request, jsonify
import pymysql
from passlib.hash import sha256_crypt
import re

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

app = Flask(__name__)

@app.route("/", methods=["GET"])
def hello():
    return "Hello, World This Is Yourney!"

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
        
@app.route('/db')
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
        return 'Invalid request'
       
    
#login
@app.route("/login",methods=["POST", "GET"])
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
        #bisa dapat di sql inject minta saran buat logika verifynya sha256_crypt.verify(password, result['password'] == result['pasword'])
        cursor.execute('SELECT * FROM user WHERE username = %s', (username, ))
        user = cursor.fetchone()
    cnx.close()
    if len(user) > 0:
        if sha256_crypt.verify(password, user[2]):
            return jsonify({'status': 'success', 'idUser': user[0], 'username': user[1]})
        else:
            return jsonify({'status': 'failed', 'message': 'Wrong password'})
    else:
        return jsonify({'status': 'failed', 'message': 'Wrong username'})
 
#register
@app.route("/register",methods=["POST", "GET"])
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
        }
    else:
        js = {
            "username": username,
            "password": Hpassword,
            "code": "sukses",
        }
    return jsonify(js)

#masih ada yang salah
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
#     with cnx.cursor() as cursor:
#         cursor.execute('SELECT * FROM user WHERE username=%s',(username))
#         user = cursor.fetchone()
#         if user:
#             js = {"code": "Account already exists !"}
#         elif not re.match(r'[A-Za-z0-9]+', username):
#             js = {"code": "Username must contain only characters and numbers !"}
#         elif not username or not password:
#             js = {"code": :"Please fill out the form !"}
#         else:
#             cursor.execute('INSERT INTO user (username, password) VALUES (%s, %s);', (username, Hpassword))
#             result = cursor.fetchone()
#             cnx.commit()
#     cnx.close()
#     #querying sql
#     # with cnx.cursor() as cursor:
#     #     cursor.execute('INSERT INTO user (username, password) VALUES (%s, %s);', (username, Hpassword))
#     #     result = cursor.fetchone()
#     #     cnx.commit()
#     # cnx.close()
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
    app.run(host='127.0.0.1', port=8080, debug=True)
