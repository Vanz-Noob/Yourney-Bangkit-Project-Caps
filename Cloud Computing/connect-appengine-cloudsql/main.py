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
import os
import re
import pymysql
from crypt import methods
from flask import Flask, request, jsonify
from flask_jwt_extended import *
from passlib.hash import sha256_crypt
from flask_swagger_ui import get_swaggerui_blueprint
from datetime import datetime, timedelta, timezone
from services.user import UserService

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')
ACCESS_EXPIRES = timedelta(hours=1)
SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = os. getcwd() + '/static/swagger.json'  # Our API url (can of course be a local resource)


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] =  str(os.environ.get("JWT_SECRET"))
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
jwt = JWTManager(app)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    },
)

app.register_blueprint(swaggerui_blueprint)

# Callback function to check if a JWT exists in the database blocklist
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    #connect database
    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                            unix_socket=unix_socket, db=db_name)

        #querying sql
    with cnx.cursor() as cursor:
        cursor.execute('SELECT * FROM TokenBlocklist WHERE jti = %s', (jti, ))
        token = cursor.fetchone()
    cnx.close()

    return token is not None

user_service = UserService(db_user,db_password,db_name,db_connection_name)

@app.route("/", methods=["GET"])
def hello():
    return "Hello, World This Is Yourney!"

#GET ALL DESTINASI
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
                destinasi.append({'id_destinasi': row[0], 'id_kategori_destinasi': row[1], 'nama_desinasi': row[2], 'deskripsi': row[3], 'pic_destinasi': row[4], 'url_destinasi': row[5]})
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
                kategori.append({'id_kategori': row[1], 'nama_kategori': row[4]})
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
                users.append({'created_time': row[2], 'id_user': row[0], 'id_kategori': row[1], 'username': row[3], 'password': row[4], 'status': row[7]})
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
    try:
        request_data = request.get_json()
        username = request_data['username']
        password = request_data['password']
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

        if not user:
            return jsonify({'status': 'failed', 'message': 'no active user found'}),401

        if not sha256_crypt.verify(password, user[5]):
            return jsonify({'status': 'failed', 'message': 'either username or password is invalid'}),401
        
        # generate new token
        expires = timedelta(days=1)
        expires_refresh = timedelta(days=3)
        identity = {
            'user_id': user[0],
            'username': user[4]
        }
        access_token = create_access_token(identity=identity, fresh=True, expires_delta=expires)
        refresh_token = create_refresh_token(identity=identity, expires_delta=expires_refresh)

        return jsonify(
            {
                'status': 'success',
                'access': access_token,
                'refresh': refresh_token
            }
        ),201

    except Exception as e:
        return jsonify(
            {
                "message": str(e)
            }
        ),500

@app.route("/refresh", methods=["POST"])
def refresh():
    return user_service.refresh()

@app.route("/logout", methods=["DELETE"])
@jwt_required(verify_type=False)
def logout():
    token = get_jwt()
    jti = token["jti"]
    ttype = token["type"]
    now = datetime.now(timezone.utc)

    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                            unix_socket=unix_socket, db=db_name)
    with cnx.cursor() as cursor:
        cursor.execute('INSERT INTO TokenBlocklist(jti,type,created_at) VALUES (%s, %s, %s);', (jti, ttype, now))
        cnx.commit()
    cnx.close()
    return jsonify({"msg": "logout successful"})

# endpoint to verify jwt token works properly
# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/protected", methods=["GET"])
@jwt_required(refresh=False)
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user['username']), 200
    
    
 #register user + initialiazing kategori
@app.route("/register",methods=["POST", "GET"])
def register():
    try:
        request_data = request.get_json()
        username = request_data['username']
        email = request_data['email']
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
        #validation
        # password
        if not re.fullmatch(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$', password):
            return jsonify(
                {
                    'message': 'password character must be atleast 8 character with capital case and number charachter'
                }
            ), 400

        # email
        emailformat = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if not re.fullmatch(emailformat, email):
            return jsonify(
                {
                    'message': 'email is not in valid format'
                }
            ), 400
        # validate if email or username is used
        exist = user_service.check_existing_user(username, email)

        if exist:
            return jsonify(
                {
                    'message': 'user already exist'
                }
            ), 400

        #querying sql
        with cnx.cursor() as cursor:
            cursor.execute('INSERT INTO user (username, email, password, jenis_kelamin, tempat_lahir) VALUES (%s, %s, %s, %s, %s);', (username, email, Hpassword, jenis_kelamin, tempat_lahir))
            cnx.commit()
            cursor.execute('SELECT id_user FROM user WHERE username=%s;',(username))
            id_user = cursor.fetchone()
            cursor.execute('INSERT INTO kategori(id_kategori_user) VALUES(%s);', (id_user))
            cnx.commit()
            cursor.execute('UPDATE user SET id_kategori1=%s WHERE id_user=%s;', (id_user, id_user))
            cnx.commit()
            result = cursor.fetchone()
        cnx.close()
        
        # if result:
        #     js = {
        #         "username": username,
        #         "password": Hpassword,
        #         "jenis_kelamin" : jenis_kelamin,
        #         "tempat_lahir" : tempat_lahir,
        #         "code": "sukses",
        #     }
        # else:
        #     js = {
        #         "code": "gagal",
        #     },400
        return jsonify({
                "username": username,
                    "jenis_kelamin" : jenis_kelamin,
                "tempat_lahir" : tempat_lahir,
                "code": "sukses",
            })
    except Exception as e:
        return jsonify({
            "message": str(e)
        })

# # update category to user
# @app.route("/UpdateKateUser",methods=["POST", "GET"])
# def UpdateKateUser():
#     request_data = request.get_json()
#     id_user = request_data['id_user']
#     id_kategori1 = request_data['id_kategori1']
    
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
#         cursor.execute('UPDATE user SET id_kategori1=%s WHERE id_user=%s ;', (id_kategori1, id_user))
#         result = cursor.fetchone()
#         cnx.commit()
#     cnx.close()
    
#     if result == 0:
#         js = {
#             "code": "gagal",
#         }
#     else:
#         js = {
#             "code": "sukses",
#         }
#     return jsonify(js)

# change status admin user
@app.route("/UpStatUser",methods=["POST", "GET"])
def UpStatUser():
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

#adding destinasi sesuai kategori
@app.route("/addDest",methods=["POST", "GET"])
def addDest():
    request_data = request.get_json()
    id_kategori_destinasi = request_data['id_kategori_destinasi']
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
        cursor.execute('INSERT INTO destinasi (id_kategori_destinasi, nama_destinasi, deskripsi, pic_destinasi, url_destinasi) VALUES (%s, %s, %s, %s, %s);', (id_kategori_destinasi, nama_destinasi, deskripsi, pic_destinasi, url_destinasi))
        result = cursor.fetchone()
        cnx.commit()
    cnx.close()
    
    if result == 0:
        js = {
            "code": "gagal",
        }
    else:
        js = {
            "id_kategori_destinasi" : id_kategori_destinasi,
            "nama_destinasi": nama_destinasi,
            "deskripsi": deskripsi,
            "URL gambar" : pic_destinasi,
            "URL destinasi" : url_destinasi,
            "code": "sukses",
        }
    return jsonify(js)

#adding kategori user
@app.route("/addKate",methods=["POST", "GET"])
def addKate():
    request_data = request.get_json()
    id_kategori_user = request_data['id_kategori_user']
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
        cursor.execute('UPDATE kategori SET id_kategori=%s, nama_kategori=%s where id_kategori_user=%s;', (id_kategori, nama_kategori, id_kategori_user))
        result = cursor.fetchone()
        cnx.commit()
    cnx.close()
    
    if result == 0:
        js = {
            "code": "gagal",
        }
    else:
        js = {
            "id_kategori_user" : id_kategori_user,
            "id_kategori": id_kategori,
            "nama_kategori": nama_kategori
        }
    return jsonify(js)

#update id dataset tabel kategori
@app.route("/updateKateSet",methods=["POST", "GET"])
def updateKateSet():
    request_data = request.get_json()
    id_kategori_user = request_data['id_kategori_user']
    id_kategori_dataset = request_data['id_kategori_dataset']
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
        cursor.execute('INSERT INTO dataset (id_kategori_dataset, cleaned_tweet) VALUES (%s, %s);', (id_kategori_dataset, cleaned_tweet))
        cursor.execute('SELECT id_dataset FROM dataset ORDER BY id_dataset DESC LIMIT 1;')
        max_id = cursor.fetchone()
        cursor.execute('UPDATE kategori SET id_dataset1=%s WHERE id_kategori_user=%s;', (max_id, id_kategori_user))
        result =cursor.fetchone()
        cnx.commit()
    cnx.close()
    
    if result == 0:
        js = {
            "code": "gagal",
        }
    else:
        js = {
            "id_kategori_user" : id_kategori_user,
            "id_kategori_dataset" : id_kategori_dataset,
            "cleaned_tweet" : cleaned_tweet,
            "code" : "berhasil"
        }
    return jsonify(js)

# #adding dataset
# @app.route("/addData",methods=["POST", "GET"])
# def addData():
#     request_data = request.get_json()
#     id_kategori_dataset = request_data['id_kategori_dataset']
#     cleaned_tweet = request_data['cleaned_tweet']
    
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
#         cursor.execute('INSERT INTO dataset (id_kategori_dataset, cleaned_tweet) VALUES(%s, %s);', (id_kategori_dataset, cleaned_tweet))
#         result = cursor.fetchone()
#         cnx.commit()
#     cnx.close()
    
#     if result == 0:
#         js = {
#             "code": "gagal",
#         }
#     else:
#         js = {
#             "id_kategori_dataset": id_kategori_dataset,
#             "cleaned_tweet": cleaned_tweet
#         }
#     return jsonify(js)

# @app.route('/GetDesc',methods=["POST", "GET"])
# def GetDesc():
#     request_data = request.get_json()
#     nama_destinasi = request_data['nama_destinasi']
#     deskripsi = []
#     if request.method == 'GET':
#         if os.environ.get('GAE_ENV') == 'standard':
#             # If deployed, use the local socket interface for accessing Cloud SQL
#             unix_socket = '/cloudsql/{}'.format(db_connection_name)
#             cnx = pymysql.connect(user=db_user, password=db_password,
#                                 unix_socket=unix_socket, db=db_name)
#         with cnx.cursor() as cursor:
#             cursor.execute('SELECT deskripsi FROM destinasi WHERE nama_destinasi=%s;', (nama_destinasi))
#             result =cursor.fetchone()
#             deskripsi.append({result})

#dapatin deskripsi dari nama destinasi tertentu
@app.route("/GetDesc",methods=["POST", "GET"])
def GetDesc():
    request_data = request.get_json()
    nama_destinasi = request_data['nama_destinasi']

    
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
        cursor.execute('SELECT deskripsi FROM destinasi WHERE nama_destinasi=%s;', (nama_destinasi))
        result = cursor.fetchone()
        cnx.commit()
    cnx.close()
    
    if result == 0:
        js = {
            "code": "gagal",
        }
    else:
        js = {
            "deskripsi": result,
        }
    return jsonify(js)      

#search destinasi
@app.route('/search',methods=["GET"])
def search():
    # request_data = request.get_json()
    # nama_destinasi = request_data['nama_destinasi']
    search = []
    # if request.method == 'POST':
    #     if os.environ.get('GAE_ENV') == 'standard':
    #         # If deployed, use the local socket interface for accessing Cloud SQL
    #         unix_socket = '/cloudsql/{}'.format(db_connection_name)
    #         cnx = pymysql.connect(user=db_user, password=db_password,
    #                             unix_socket=unix_socket, db=db_name)
    # #     with cnx.cursor() as cursor:
    # #         cursor.execute('SELECT * FROM destinasi WHERE nama_destinasi LIKE %s ORDER BY nama_destinasi;', (nama_destinasi))
    # #         result = cursor.fetchall()
    # #     cnx.close()
    # #     return jsonify(result)
    # # else:
    # #     return 'invalid request'
    #     with cnx.cursor() as cursor:
    #         cursor.execute('SELECT * FROM destinasi WHERE LOWER(nama_destinasi) LIKE LOWER(%s) ORDER BY nama_destinasi;', (nama_destinasi))
    #         for row in cursor:
    #             search.append({'id_destinasi': row[0], 'id_kategori_destinasi': row[1], 'nama_desinasi': row[2], 'deskripsi': row[3], 'pic_destinasi': row[4], 'url_destinasi': row[5]})
    #         cnx.close()
    #     return jsonify(search)
    # else:
    #     return 'Invalid request'
    args = request.args
    nama_destinasi = f"%{args.get('nama_destinasi')}%"
    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                            unix_socket=unix_socket, db=db_name)
    with cnx.cursor() as cursor:
        cursor.execute('SELECT * FROM destinasi WHERE LOWER(nama_destinasi) LIKE LOWER(%s) ORDER BY nama_destinasi;', (nama_destinasi))
        for row in cursor:
            search.append({'id_destinasi': row[0], 'id_kategori_destinasi': row[1], 'nama_desinasi': row[2], 'deskripsi': row[3], 'pic_destinasi': row[4], 'url_destinasi': row[5]})
        cnx.close()
    return jsonify(search)


    
        

    
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
