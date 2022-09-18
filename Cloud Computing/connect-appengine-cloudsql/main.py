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

#cek DB
@app.route('/db')
def db():
    # sudah okay
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
                users.append(
                    {'idUser': row[0], 'username': row[1], 'password': row[2]})
            cnx.close()
        return jsonify(users)
    else:
        return 'Invalid request'

# cek destinasi
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
                destinasi.append(
                    {'id_destinasi': row[0], 'nama_destinasi': row[2], 'deskripsi': row[3]})
            cnx.close()
        return jsonify(destinasi)
    else:
        return 'Invalid request'
    
# adding destinasi
@app.route("/addDest", methods=["POST", "GET"])
def destinasi():
    request_data = request.get_json()
    deskripsi = request_data['destinasi']
    id_destinasi = request_data['id_destinasi']
    nama_destinasi = request_data['nama_destinasi']

    # connect database
    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    else:
        host = '127.0.0.1'
        cnx = pymysql.connect(user=db_user, password=db_password,
                              host=host, db=db_name)
    # querying sql
    with cnx.cursor() as cursor:
        cursor.execute('INSERT INTO destinasi (nama_destinasi, deskripsi) VALUES (%s, %s);',
                       (nama_destinasi, deskripsi))
        result = cursor.fetchone()
        cnx.commit()
    cnx.close()

    if result == 0:
        js = {
            "code": "gagal",
        }
    else:
        js = {
            "deskripsi": deskripsi,
            "id_destinasi": id_destinasi,
            "nama_destinasi": nama_destinasi
        }
    return jsonify(js)

# # cek kategori
# @app.route('/kategori')
# def kategori():
#     kategori = []
#     if request.method == 'GET':
#         if os.environ.get('GAE_ENV') == 'standard':
#             # If deployed, use the local socket interface for accessing Cloud SQL
#             unix_socket = '/cloudsql/{}'.format(db_connection_name)
#             cnx = pymysql.connect(user=db_user, password=db_password,
#                                   unix_socket=unix_socket, db=db_name)
#         with cnx.cursor() as cursor:
#             cursor.execute('SELECT * FROM kategori;')
#             for row in cursor:
#                 kategori.append(
#                     {'id_kategori': row[0], 'nama_kategori': row[1]})
#             cnx.close()
#         return jsonify(kategori)
#     else:
#         return 'Invalid request'

# # adding kategori
# @app.route("/addkate", methods=["POST", "GET"])
# def kategori():
#     request_data = request.get_json()
#     id_kategori = request_data['id_kategori']
#     nama_kategori = request_data['nama_kategori']

#     # connect database
#     if os.environ.get('GAE_ENV') == 'standard':
#         unix_socket = '/cloudsql/{}'.format(db_connection_name)
#         cnx = pymysql.connect(user=db_user, password=db_password,
#                               unix_socket=unix_socket, db=db_name)
#     else:
#         host = '127.0.0.1'
#         cnx = pymysql.connect(user=db_user, password=db_password,
#                               host=host, db=db_name)
#     # querying sql
#     with cnx.cursor() as cursor:
#         cursor.execute(
#             'INSERT INTO kategori (nama_kategori) VALUES (%s);', 
#             (nama_kategori))
#         result = cursor.fetchone()
#         cnx.commit()
#     cnx.close()

#     if result == 0:
#         js = {
#             "code": "gagal",
#         }
#     else:
#         js = {
#             "id_kategori": id_kategori,
#             "nama_kategori": nama_kategori
#         }
#     return jsonify(js)

# login
@app.route("/login", methods=["POST", "GET"])
def login():
    try:

        request_data = request.get_json()
        username = request_data['username']
        password = request_data['password']
        Hpassword = sha256_crypt.encrypt(password)
        # connect database
        if os.environ.get('GAE_ENV') == 'standard':
            unix_socket = '/cloudsql/{}'.format(db_connection_name)
            cnx = pymysql.connect(user=db_user, password=db_password,
                                  unix_socket=unix_socket, db=db_name)

        # querying sql
        with cnx.cursor() as cursor:
            cursor.execute(
                'SELECT * FROM user WHERE username = %s', (username, ))
            user = cursor.fetchone()
        cnx.close()
        if len(user) > 0:
            if sha256_crypt.verify(password, user[2]):
                resp = jsonify(
                    {'status': 'success', 'idUser': user[0], 'username': user[1]})
                resp.status_code = 200
                return resp
            else:
                resp = jsonify(
                    {'status': 'failed', 'message': 'Wrong password'})
                resp.status_code = 401
                return resp
        else:
            resp = jsonify({'status': 'failed', 'message': 'Wrong username'})
            resp.status_code = 400
            return resp

    except Exception as e:
        print(e)

    finally:
        if cnx.is_connected():
            cnx.close()
            print('MySQL connection is closed')
            
# register
@app.route("/register", methods=["POST", "GET"])
def register():
    request_data = request.get_json()
    username = request_data['username']
    password = request_data['password']
    Hpassword = sha256_crypt.encrypt(password)

    # connect database
    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    else:
        host = '127.0.0.1'
        cnx = pymysql.connect(user=db_user, password=db_password,
                              host=host, db=db_name)
    # querying sql
    with cnx.cursor() as cursor:
        cursor.execute(
            'INSERT INTO user (username, password) VALUES (%s, %s);', (username, Hpassword))
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




if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
