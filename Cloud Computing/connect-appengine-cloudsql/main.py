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
from datetime import datetime

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

app = Flask(__name__)

@app.route("/", methods=["GET"])
def hello():
    return "Hello, World This Is Yourney!"

#cek destinasi
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
                destinasi.append({'id_destinasi': row[0], 'id_kategori': row[1], 'nama_desinasi': row[2], 'deskripsi': row[3]})
            cnx.close()
        return jsonify(destinasi)
    else:
        return 'Invalid request'  
    
#cek kategori
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
                kategori.append({'id_kategori': row[0], 'id_dataset': row[1], 'id_destinasi': row[2], 'nama_kategori': row[3]})
            cnx.close()
        return jsonify(kategori)
    else:
        return 'Invalid request'  


# cek db user
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
                users.append({'id_user': row[0], 'id_kategori': row[1], 'username': row[3], 'password': row[4], 'status': row[5]})
            cnx.close()
        return jsonify(users)
    else:
        return 'Invalid request'
    
# cek dataset
@app.route('/dataset')
def dataset():
    #sudah okay
    users = []
    if request.method == 'GET':
        if os.environ.get('GAE_ENV') == 'standard':
            # If deployed, use the local socket interface for accessing Cloud SQL
            unix_socket = '/cloudsql/{}'.format(db_connection_name)
            cnx = pymysql.connect(user=db_user, password=db_password,
                                unix_socket=unix_socket, db=db_name)
        with cnx.cursor() as cursor:
            cursor.execute('SELECT * FROM dataset;')
            for row in cursor:
                users.append({'id_dataset': row[0], 'id_kategori': row[1], 'cleaned_tweet': row[2]})
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
    jenis_kelamin = request_data['jenis_kelamin']
    tempat_lahir = request_data['tempat_lahir']
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
        cursor.execute('INSERT INTO user (username, password, jenis_kelamin, tempat_lahir) VALUES (%s, %s, %s, %s);', (username, Hpassword, jenis_kelamin, tempat_lahir))
        result = cursor.fetchone()
        cnx.commit()
        cursor.execute('SELECT id_user FROM user WHERE username=%s;',(username))
        id_user = cursor.fetchone()
        cursor.execute('INSERT INTO kategori(id_kategori_user) VALUES(%s);', (id_user))
        cursor.execute('UPDATE user SET id_kategori1=%s WHERE id_user=%s;', (id_user, id_user))
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
            "jeniskelamin" : jenis_kelamin,
            "tempatlahir" : tempat_lahir,
            "code": "sukses",
        }
    return jsonify(js)


# adding category to user
@app.route("/addKateUser",methods=["POST", "GET"])
def addKateUserr():
    request_data = request.get_json()
    id_user = request_data['id_user']
    id_kategori1 = request_data['id_kategori1']
    
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
        cursor.execute('UPDATE user SET id_kategori1=%s WHERE id_user=%s ;', (id_kategori1, id_user))
        result = cursor.fetchone()
        cnx.commit()
    cnx.close()
    
    if result == 0:
        js = {
            "code": "gagal",
        }
    else:
        js = {
            "code": "sukses",
        }
    return jsonify(js)

# change status user
@app.route("/addKateUser",methods=["POST", "GET"])
def addKateUserr():
    request_data = request.get_json()
    id_user = request_data['id_user']
    status = request_data['status']
    
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
        cursor.execute('UPDATE user SET status=%s WHERE id_user=%s ;', (status, id_user))
        result = cursor.fetchone()
        cnx.commit()
    cnx.close()
    
    if result == 0:
        js = {
            "code": "gagal",
        }
    else:
        js = {
            "code": "sukses",
        }
    return jsonify(js)

#adding destinasi
@app.route("/addDest",methods=["POST", "GET"])
def addDest():
    request_data = request.get_json()
    id_kategori2 = request_data['id_kategori2']
    nama_destinasi = request_data['nama_destinasi']
    deskripsi = request_data['deskripsi']
    pic_destinasi = request_data['pic_destinasi']
    url_destinasi = request_data['url_destinasi']
    
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
        cursor.execute('INSERT INTO destinasi (id_kategori2, nama_destinasi, deskripsi, pic_destinasi, url_destinasi) VALUES (%s, %s, %s, %s, %s);', (id_kategori2, nama_destinasi, deskripsi, pic_destinasi, url_destinasi))
        result = cursor.fetchone()
        cnx.commit()
    cnx.close()
    
    if result == 0:
        js = {
            "code": "gagal",
        }
    else:
        js = {
            "id_kategori" : id_kategori2,
            "nama_destinasi": nama_destinasi,
            "deskripsi": deskripsi,
            "URL gambar" : pic_destinasi,
            "URL destinasi" : url_destinasi,
            "code": "sukses",
        }
    return jsonify(js)

#adding kategori
@app.route("/addKate",methods=["POST", "GET"])
def addKate():
    request_data = request.get_json()
    id_kategori = request_data['id_kategori']
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
        cursor.execute('INSERT INTO kategori (id_kategori, nama_kategori) VALUES (%s, %s);', (id_kategori, nama_kategori))
        result = cursor.fetchone()
        cnx.commit()
    cnx.close()
    
    if result == 0:
        js = {
            "code": "gagal",
        }
    else:
        js = {
            "id_kategori": id_kategori,
            "nama_kategori": nama_kategori
        }
    return jsonify(js)

#update tabel kategori
@app.route("/updateKate",methods=["POST", "GET"])
def updateKate():
    request_data = request.get_json()
    id_kategori_user = request_data['id_kategori_user']
    id_dataset1 = request_data['id_dataset1']
    id_destinasi1 = request_data['id_destinasi1']
    
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
        cursor.execute('UPDATE kategori SET id_dataset1=%s, id_destinasi1=%s WHERE id_kategori_user=%s ;', (id_dataset1, id_destinasi1, id_kategori_user))
        result = cursor.fetchone()
        cnx.commit()
    cnx.close()
    
    if result == 0:
        js = {
            "code": "gagal",
        }
    else:
        js = {
            "code" : "berhasil"
        }
    return jsonify(js)

#adding dataset
@app.route("/addData",methods=["POST", "GET"])
def addData():
    request_data = request.get_json()
    id_kategori3 = request_data['id_kategori3']
    cleaned_tweet = request_data['cleaned_tweet']
    
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
        cursor.execute('INSERT INTO dataset (id_kategori3, cleaned_tweet) VALUES (%s, %s);', (id_kategori3, cleaned_tweet))
        result = cursor.fetchone()
        cnx.commit()
    cnx.close()
    
    if result == 0:
        js = {
            "code": "gagal",
        }
    else:
        js = {
            "id_kategori": id_kategori3,
            "cleaned_tweet": cleaned_tweet
        }
    return jsonify(js)




if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
