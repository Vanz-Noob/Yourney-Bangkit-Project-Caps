from crypt import methods
from msilib.schema import Binary, File
# import db
import os
from re import S
# import uuid
import pymysql
from unittest import result
from passlib.hash import sha256_crypt
from webbrowser import get
from flask import Flask, jsonify, request, make_response
# from flask_sqlalchemy import SQLAlchemy
from db import get_destinasi, get_kategori, post_destinasi, post_kategori, get_db, open_conn

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

# convert data blob menjadi binary
def InsertBlob(FilePath):
    with open(FilePath, "rb") as File:
        BinaryData = File.read()
    return BinaryData

# dapatin file image dengan passing nilai id_destinasi
def RetrieveBlobImage(ID):
    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                                unix_socket=unix_socket, db=db_name)

    #querying sql
    with cnx.cursor() as cursor:
        cursor.execute("SELECT * FROM destinasi WHERE id_destinasi= '{0}'")
        result = cursor.fetchone()[4]
        StoredFilePath = "Outputs/img{0}.jpg".format(str(ID))
        print(result)
        with open(StoredFilePath, "wb") as File:
            File.write(result)
    cnx.close()


# cek API
app = Flask(__name__)
@app.route('/', methods=['GET'])
def hello():
    return jsonify({"message" : "hello world"})

# get DB
@app.route('/db', methods=['GET'])
def get_user():
    return get_db()

# cek DB destinasi
@app.route('/destinasi', methods=['GET'])
def destinasi():
    return get_destinasi()

# tambah destinasi ke DB
@app.route('/addDest', methods=['POST'])
def addDest():
    request_data = request.get_json()
    deskripsi = request_data['deskripsi']
    nama_destinasi = request_data['nama_destinasi']
    InsertBlob(deskripsi)
    
    #connect database
    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)

    #querying sql
    with cnx.cursor() as cursor:
        cursor.execute('INSERT INTO destinasi (nama_destinasi, deskripsi) VALUES (%s, %s);', (nama_destinasi, InsertBlob))
        result = cursor.fetchone()
        cnx.commit()
    cnx.close()
    if result == 0:
        js = {
            "code": "gagal",
        }
    else:
        js = {
            "nama_destinasi": nama_destinasi,
            "code": "sukses",
        }
    return jsonify(js)
    
    
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



#login
@app.route("/login",methods=["POST"])
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
    
    
if __name__ == '__main__':
    app.run()