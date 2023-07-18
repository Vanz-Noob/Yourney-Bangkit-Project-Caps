import os
import re
from flask_cors import CORS, cross_origin
# import threading
import pymysql
import base64
import uuid
import io
from flask import Flask, request, jsonify, send_file, make_response
from werkzeug.utils import secure_filename
from flask_jwt_extended import *
from passlib.hash import sha256_crypt
from flask_swagger_ui import get_swaggerui_blueprint
from datetime import datetime, timedelta, timezone
from services.user import UserService
from services.dataset import DatasetService
from services.twitter import average_data, update_dataset


db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ACCESS_EXPIRES = timedelta(hours=1)
SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/spec.json'  # Our API url (can of course be a local resource)
user_service = UserService(db_user,db_password,db_name,db_connection_name)
data_service = DatasetService(db_user,db_password,db_name,db_connection_name)

app = Flask(__name__)
CORS(app)
CORS = CORS(app)

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1000 * 1000
app.config["JWT_SECRET_KEY"] =  str(os.environ.get("JWT_SECRET"))
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
jwt = JWTManager(app)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Yourney api"
    },
)

app.register_blueprint(swaggerui_blueprint)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Callback function to check if a JWT exists in the database blocklist
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]

    if os.environ.get("GAE_ENV") == "standard":
        unix_socket = f"/cloudsql/{db_connection_name}"
        cnx = pymysql.connect(
            user=db_user, password=db_password, unix_socket=unix_socket, db=db_name
        )
    else:
        host = "127.0.0.1"
        cnx = pymysql.connect(user=db_user, password=db_password, host=host, db=db_name)

        #querying sql
    with cnx.cursor() as cursor:
        cursor.execute('SELECT * FROM tokenblocklist WHERE jti = %s', (jti, ))
        token = cursor.fetchone()
    cnx.close()
    return token is not None

@app.route("/", methods=["GET"])
def hello():
    return "Hello, World This Is Yourney!"

@app.route("/user/likes", methods=["GET"])
@jwt_required(refresh=False)
def get_likes():
    if request.method == 'GET':
        current_user = get_jwt_identity()
        id_user = current_user['id_user']
        if os.environ.get("GAE_ENV") == "standard":
            unix_socket = f"/cloudsql/{db_connection_name}"
            cnx = pymysql.connect(
                user=db_user, password=db_password, unix_socket=unix_socket, db=db_name
            )
        else:
            host = "127.0.0.1"
            cnx = pymysql.connect(user=db_user, password=db_password, host=host, db=db_name)
        destinasi = []
        with cnx.cursor() as cursor:
            cursor.execute('SELECT destinasi.* FROM user_liked LEFT JOIN destinasi ON user_liked.id_destination_like = destinasi.id_destinasi WHERE user_liked.id_user_liked=%s', (id_user))
            for row in cursor:
                destinasi.append({'id_destinasi': row[0], 'id_kategori_destinasi': row[1], 'nama_desinasi': row[2], 'deskripsi': row[3], 'pic_destinasi': row[4], 'url_destinasi': row[5]})
            cnx.close()
        return jsonify(destinasi)

#GET ALL DESTINASI
@app.route('/destinasi')
@jwt_required(refresh=False)
def destinasi():
    if request.method == 'GET':
        query = request.args
        destinasi = []
        if os.environ.get("GAE_ENV") == "standard":
            unix_socket = f"/cloudsql/{db_connection_name}"
            cnx = pymysql.connect(
                user=db_user, password=db_password, unix_socket=unix_socket, db=db_name
            )
        else:
            host = "127.0.0.1"
            cnx = pymysql.connect(user=db_user, password=db_password, host=host, db=db_name)
        sql = 'SELECT * FROM destinasi '
        payload = []
        if query.get('category'):
            idd = '0'
            text =  query.get('category')
            if text.lower() == 'kuliner':
                idd = '1'
            elif text.lower() == 'pantai':
                idd = '2'

            sql += 'WHERE id_kategori_destinasi = %s'
            payload.append(idd)
            payload = tuple(payload)
        sql += ';'

        with cnx.cursor() as cursor:
            cursor.execute(sql, payload)
            for row in cursor:
                destinasi.append({'id_destinasi': row[0], 'id_kategori_destinasi': row[1], 'nama_desinasi': row[2], 'deskripsi': row[3], 'pic_destinasi': row[4], 'url_destinasi': row[5]})
            cnx.close()
        return jsonify(destinasi)
    else:
        return 'Invalid request'

@app.route('/destinasi/<int:destinasi_id>')
@jwt_required(refresh=False)
def destinasi_detail(destinasi_id):
    if request.method == 'GET':
        if os.environ.get("GAE_ENV") == "standard":
            unix_socket = f"/cloudsql/{db_connection_name}"
            cnx = pymysql.connect(
                user=db_user, password=db_password, unix_socket=unix_socket, db=db_name
            )
        else:
            host = "127.0.0.1"
            cnx = pymysql.connect(user=db_user, password=db_password, host=host, db=db_name)

        sql = 'SELECT * FROM destinasi WHERE id_destinasi = %s'

        #destinasi_id diganti id_destinasi?
        with cnx.cursor() as cursor:
            cursor.execute(sql, (destinasi_id, ))
            data = cursor.fetchone()
        cnx.close()

        if data:
            return jsonify({
                'id_destinasi': data[0],
                'id_kategori_destinasi': data[1],
                'nama_desinasi': data[2],
                'deskripsi': data[3],
                'pic_destinasi': data[4],
                'url_destinasi': data[5]
            })

    else:
        return 'Invalid request'


#DESTINASI LIKES api
@app.route('/destinasi/<int:destinasi_id>/likes', methods=['GET','POST','DELETE'])
@jwt_required(refresh=False)
def destinasi_likes(destinasi_id):
    if os.environ.get("GAE_ENV") == "standard":
        unix_socket = f"/cloudsql/{db_connection_name}"
        cnx = pymysql.connect(
            user=db_user, password=db_password, unix_socket=unix_socket, db=db_name
        )
    else:
        host = "127.0.0.1"
        cnx = pymysql.connect(user=db_user, password=db_password, host=host, db=db_name)
    current_user = get_jwt_identity()
    user = current_user['id_user']
    likes = []
    if request.method == 'GET':

        with cnx.cursor() as cursor:
            cursor.execute('SELECT * FROM user_liked WHERE id_user_liked=%s AND id_destination_like=%s;',(user,destinasi_id))
            liked = cursor.fetchone()
        cnx.close()
        if liked:
            return jsonify({
                'liked' : True
            }),200
        else:
            return jsonify({
                'message': 'data not found'
            }),404
    elif request.method == 'POST':
        with cnx.cursor() as cursor:
            cursor.execute('SELECT * FROM user_liked WHERE id_user_liked=%s AND id_destination_like=%s;',(user,destinasi_id))
            result = cursor.fetchone()
            if result:
                cursor.execute('SELECT * FROM user_liked WHERE id_user_liked=%s;',(user))
                for row in cursor:
                    likes.append({'id_user':row[1], 'id_destinasi_liked':row[2]})
                cnx.close()
                return jsonify({'likes': likes}), 200
            cursor.execute('INSERT INTO user_liked(id_user_liked,id_destination_like) VALUES (%s, %s);', (user, destinasi_id))
            cnx.commit()
            cursor.execute('SELECT * FROM user_liked WHERE id_user_liked=%s AND id_destination_like=%s;',(user,destinasi_id))
            liked=cursor.fetchone()
        cnx.close()
            
        if liked:
            return jsonify({
                'message':'destination like success'
            }),200
        else:
            return jsonify({
                'message':'destination like failed'
            }),400

    elif request.method == 'DELETE':
        try:

            with cnx.cursor() as cursor:
                cursor.execute('DELETE FROM user_liked WHERE id_user_liked=%s AND id_destination_like=%s;',(user,destinasi_id))
                cnx.commit()
            cnx.close()

            return jsonify({
                'message':'destination delete success'
            }),200
        except Exception as e:
            return jsonify({
                'message': str(e)
            }),400

    else:
        return 'Invalid request'

#cek kategori
@app.route('/kategori')
@jwt_required(refresh=False)
def kategori():
    kategori = []
    if request.method == 'GET':
        if os.environ.get("GAE_ENV") == "standard":
            unix_socket = f"/cloudsql/{db_connection_name}"
            cnx = pymysql.connect(
                user=db_user, password=db_password, unix_socket=unix_socket, db=db_name
            )
        else:
            host = "127.0.0.1"
            cnx = pymysql.connect(user=db_user, password=db_password, host=host, db=db_name)
        with cnx.cursor() as cursor:
            cursor.execute('SELECT id_kategori, nama_kategori FROM kategori;')
            for row in cursor:
                kategori.append({'id_kategori': row[0], 'nama_kategori': row[1]})
            cnx.close()
        return jsonify(kategori)
    else:
        return 'Invalid request'  


# cek db user
@app.route('/db')
@jwt_required(refresh=False)
def db():
    #sudah okay
    users = []
    if request.method == 'GET':
        if os.environ.get("GAE_ENV") == "standard":
            unix_socket = f"/cloudsql/{db_connection_name}"
            cnx = pymysql.connect(
                user=db_user, password=db_password, unix_socket=unix_socket, db=db_name
            )
        else:
            host = "127.0.0.1"
            cnx = pymysql.connect(user=db_user, password=db_password, host=host, db=db_name)
        with cnx.cursor() as cursor:
            cursor.execute('SELECT * FROM user;')
            for row in cursor:
                users.append({'created_time': row[3], 'id_user': row[0], 'id_kategori': row[1], 
                              'username': row[5], 'email':row[10], 'usename_twitter':row[12], 'status': row[7]})
            cnx.close()
        return jsonify(users)
    else:
        return 'Invalid request'

# cek dataset
@app.route('/dataset',methods=['GET','POST'])
@jwt_required(refresh=False)
def dataset():
    #sudah okay
    datasets = []
    if request.method == 'GET':
        if os.environ.get("GAE_ENV") == "standard":
            unix_socket = f"/cloudsql/{db_connection_name}"
            cnx = pymysql.connect(
                user=db_user, password=db_password, unix_socket=unix_socket, db=db_name
            )
        else:
            host = "127.0.0.1"
            cnx = pymysql.connect(user=db_user, password=db_password, host=host, db=db_name)
        with cnx.cursor() as cursor:
            cursor.execute('SELECT * FROM dataset;')
            for row in cursor:
                datasets.append({'created_time': row[0], 'author': row[1], 'tweet': row[2], 'kategori': row[3]})
            cnx.close()
        return jsonify(datasets)
    else:
        return 'Invalid request'
       
    
#login
@app.route("/login",methods=["POST", "GET"])
@cross_origin()
def login():
    try:
        request_data = request.get_json()
        username = request_data['username']
        password = request_data['password']
        #connect database
        if os.environ.get("GAE_ENV") == "standard":
            unix_socket = f"/cloudsql/{db_connection_name}"
            cnx = pymysql.connect(
            user=db_user, password=db_password, unix_socket=unix_socket, db=db_name
            )
        else:
            host = "127.0.0.1"
            cnx = pymysql.connect(user=db_user, password=db_password, host=host, db=db_name)
        #querying sql
        with cnx.cursor() as cursor:
            cursor.execute('SELECT user.*, kategori.nama_kategori FROM user LEFT JOIN kategori ON user.id_kategori1 = id_kategori_user WHERE username = %s', (username, ))
            user = cursor.fetchone()
        cnx.close()

        if not user:
            return jsonify({'status': 'failed', 'message': 'no active user found'}),401

        if not sha256_crypt.verify(password, user[6]):
            return jsonify({'status': 'failed', 'message': 'either username or password is invalid'}),401
        
        # generate new token
        expires = timedelta(days=1)
        expires_refresh = timedelta(days=3)
        identity = {
            'id_user': user[0],
            'username': user[5],
            'status':user[9]
        }

        access_token = create_access_token(identity=identity, fresh=True, expires_delta=expires)
        refresh_token = create_refresh_token(identity=identity, expires_delta=expires_refresh)
        return jsonify(
            {
                'status': 'success',
                'access': access_token,
                'refresh': refresh_token,
                'user':{
                    'username': user[5],
                    'jenis_kelamin': user[7],
                    'tempat_lahir': user[8],
                    'email':user[10],
                    'recomendation':user[13],
                    'user_pic': user[11],
                    'username_twitter': user[12]
                }
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

    if os.environ.get("GAE_ENV") == "standard":
        unix_socket = f"/cloudsql/{db_connection_name}"
        cnx = pymysql.connect(
            user=db_user, password=db_password, unix_socket=unix_socket, db=db_name
        )
    else:
        host = "127.0.0.1"
        cnx = pymysql.connect(user=db_user, password=db_password, host=host, db=db_name)

    with cnx.cursor() as cursor:
        cursor.execute('INSERT INTO tokenblocklist(jti,type,created_at) VALUES (%s, %s, %s);', (jti, ttype, now))
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

# get user profile

@app.route("/user/profile", methods=["PUT","GET"])
@jwt_required(refresh=False)
def user():
    #connect database
    if os.environ.get("GAE_ENV") == "standard":
        unix_socket = f"/cloudsql/{db_connection_name}"
        cnx = pymysql.connect(
            user=db_user, password=db_password, unix_socket=unix_socket, db=db_name
        )
    else:
        host = "127.0.0.1"
        cnx = pymysql.connect(user=db_user, password=db_password, host=host, db=db_name)
    if request.method == "GET":
        current_user = get_jwt_identity()
        id_user = current_user['id_user']

        #querying sql
        user = user_service.get_user_by_id(id_user)

        # tabelnya belum di sesuaikan
        return jsonify(
            {
                'status': 'success',
                'user':{
                    'id': user[0],
                    'full_name': user[4],
                    'username': user[5],
                    'jenis_kelamin': user[7],
                    'tempat_lahir': user[8],
                    'email':user[10],
                    'user_pic': user[11],
                    'username_twitter': user[12],
                    'recomendation': user[13]
                }
            }
        ),200

    elif request.method == "PUT":
        current_user = get_jwt_identity()
        data = request.get_json()
        id_user = current_user['id_user']

        if not data:
            return jsonify({
                'message':'empty required field'
            }), 400
        payload = []

        sql = 'UPDATE user SET '
        sqlupdated = []
        if 'full_name' in data:
            sqlupdated.append('full_name = %s ')
            payload.append(data['full_name'])
        
        if 'jenis_kelamin' in data:
            sqlupdated.append('jenis_kelamin = %s ')
            payload.append(data['jenis_kelamin'])
        
        if 'tempat_lahir' in data:
            sqlupdated.append('tempat_lahir = %s ')
            payload.append(data['tempat_lahir'])

        if 'user_pic' in data:
            sqlupdated.append('user_pic = %s ')
            payload.append(data['user_pic'])
        
        if 'username_twitter' in data:
            sqlupdated.append('username_twitter = %s ')
            payload.append(data['username_twitter'])
        
        for i in range(len(sqlupdated)):
            if i != 0:
                sql += ','
            sql+= sqlupdated[i]

        sql += 'WHERE id_user = %s;'
        payload.append(id_user)
        payload = tuple(payload)
    
        #connect database
        if os.environ.get("GAE_ENV") == "standard":
            unix_socket = f"/cloudsql/{db_connection_name}"
            cnx = pymysql.connect(
                user=db_user, password=db_password, unix_socket=unix_socket, db=db_name
            )
        else:
            host = "127.0.0.1"
            cnx = pymysql.connect(user=db_user, password=db_password, host=host, db=db_name)

        #querying sql
        with cnx.cursor() as cursor:
            cursor.execute(sql, payload)
            cursor.execute('SELECT id_user, full_name, username, tempat_lahir, email, jenis_kelamin, user_pic, username_twitter FROM user WHERE id_user=%s;',(id_user))
            cnx.commit()
            user = cursor.fetchone()
        cnx.close()

        return jsonify(
            {
                'id': user[0],
                'full_name': user[1],
                'username': user[2],
                'jenis_kelamin': user[5],
                'tempat_lahir': user[3],
                'email':user[4],
                'user_pic': user[6],
                'username_twitter': user[7]
        }
        ), 200
    else:
        return jsonify({
            'message': 'invalid method'
        }), 400



    
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
        if os.environ.get("GAE_ENV") == "standard":
            unix_socket = f"/cloudsql/{db_connection_name}"
            cnx = pymysql.connect(
                user=db_user, password=db_password, unix_socket=unix_socket, db=db_name
            )
        else:
            host = "127.0.0.1"
            cnx = pymysql.connect(user=db_user, password=db_password, host=host, db=db_name)
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


# change status admin user
@app.route("/UpStatUser",methods=["POST", "GET"])
@jwt_required(refresh=False)
def UpStatUser():
    current_user = get_jwt_identity()
    if current_user["status"] != "admin":
        js = {
            'status':'anda tidak memilki akses'
        }
        return jsonify(js),403
    request_data = request.get_json()
    id_user = request_data['id_user']
    status = request_data['status']
    
    #connect database
    if os.environ.get("GAE_ENV") == "standard":
        unix_socket = f"/cloudsql/{db_connection_name}"
        cnx = pymysql.connect(
            user=db_user, password=db_password, unix_socket=unix_socket, db=db_name
        )
    else:
        host = "127.0.0.1"
        cnx = pymysql.connect(user=db_user, password=db_password, host=host, db=db_name)
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

# edit destinasi 
@app.route("/editDest", methods=["PUT"])
@jwt_required(refresh=False)
@cross_origin()
def editDest():
    request_data = request.get_json()
    id_kategori_destinasi = request_data['id_kategori_destinasi']
    id_destinasi = request_data['id_destinasi']
    nama_destinasi = request_data['nama_destinasi']
    deskripsi = request_data['deskripsi']
    pic_destinasi = request_data['pic_destinasi']
    url_destinasi = request_data['url_destinasi']

    # Connect to the database
    if os.environ.get("GAE_ENV") == "standard":
        unix_socket = f"/cloudsql/{db_connection_name}"
        cnx = pymysql.connect(
            user=db_user, password=db_password, unix_socket=unix_socket, db=db_name
        )
    else:
        host = "127.0.0.1"
        cnx = pymysql.connect(user=db_user, password=db_password, host=host, db=db_name)

    # Query SQL
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    elif request.method == "PUT":
        with cnx.cursor() as cursor:
            cursor.execute('UPDATE destinasi SET id_kategori_destinasi=%s, nama_destinasi=%s, deskripsi=%s, pic_destinasi=%s, url_destinasi=%s WHERE id_destinasi=%s',
                        (id_kategori_destinasi, nama_destinasi, deskripsi, pic_destinasi, url_destinasi, id_destinasi))
            result = cursor.fetchone()
            cnx.commit()
        cnx.close()

        if result == 0:
            js = {
                "code": "gagal",
            }
        else:
            js = {
                "id_destinasi": id_destinasi,
                "id_kategori_destinasi": id_kategori_destinasi,
                "nama_destinasi": nama_destinasi,
                "deskripsi": deskripsi,
                "URL gambar": pic_destinasi,
                "URL destinasi": url_destinasi,
                "code": "sukses",
            }
        return jsonify(js)
    else:
        raise RuntimeError("We don't know how to handle that {}".format(request.method))


def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response




# hapus destinasi
@app.route("/delDest", methods=["DELETE"])
@jwt_required(refresh=False)
@cross_origin(origin='https://yourney-api.et.r.appspot.com/delDest')
def delDest():
    request_data = request.get_json()
    id_destinasi = request_data['id_destinasi']
    #connect database
    if os.environ.get("GAE_ENV") == "standard":
        unix_socket = f"/cloudsql/{db_connection_name}"
        cnx = pymysql.connect(
            user=db_user, password=db_password, unix_socket=unix_socket, db=db_name
        )
    else:
        host = "127.0.0.1"
        cnx = pymysql.connect(user=db_user, password=db_password, host=host, db=db_name)
        
    with cnx.cursor() as cursor:
        cursor.execute('DELETE FROM destinasi WHERE id_destinasi=%s',(id_destinasi))
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
@jwt_required(refresh=False)
@cross_origin(origin='https://yourney-api.et.r.appspot.com/addDest')
def addDest():
    request_data = request.get_json()
    id_kategori_destinasi = request_data['id_kategori_destinasi']
    nama_destinasi = request_data['nama_destinasi']
    deskripsi = request_data['deskripsi']
    pic_destinasi = request_data['pic_destinasi']
    url_destinasi = request_data['url_destinasi']
    
    #connect database
    if os.environ.get("GAE_ENV") == "standard":
        unix_socket = f"/cloudsql/{db_connection_name}"
        cnx = pymysql.connect(
            user=db_user, password=db_password, unix_socket=unix_socket, db=db_name
        )
    else:
        host = "127.0.0.1"
        cnx = pymysql.connect(user=db_user, password=db_password, host=host, db=db_name)
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
@jwt_required(refresh=False)
def addKate():
    request_data = request.get_json()
    id_kategori_user = request_data['id_kategori_user']
    id_kategori = request_data['id_kategori']
    nama_kategori = request_data['nama_kategori']
    
    #connect database
    if os.environ.get("GAE_ENV") == "standard":
        unix_socket = f"/cloudsql/{db_connection_name}"
        cnx = pymysql.connect(
            user=db_user, password=db_password, unix_socket=unix_socket, db=db_name
        )
    else:
        host = "127.0.0.1"
        cnx = pymysql.connect(user=db_user, password=db_password, host=host, db=db_name)
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
@jwt_required(refresh=False)
def updateKateSet():
    request_data = request.get_json()
    id_kategori_user = request_data['id_kategori_user']
    id_kategori_dataset = request_data['id_kategori_dataset']
    cleaned_tweet = request_data['cleaned_tweet']
    
    #connect database
    if os.environ.get("GAE_ENV") == "standard":
        unix_socket = f"/cloudsql/{db_connection_name}"
        cnx = pymysql.connect(
            user=db_user, password=db_password, unix_socket=unix_socket, db=db_name
        )
    else:
        host = "127.0.0.1"
        cnx = pymysql.connect(user=db_user, password=db_password, host=host, db=db_name)
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

#dapatin deskripsi dari nama destinasi tertentu
@app.route("/GetDesc",methods=["POST", "GET"])
@jwt_required(refresh=False)
def GetDesc():
    request_data = request.get_json()
    nama_destinasi = request_data['nama_destinasi']

    
    #connect database
    if os.environ.get("GAE_ENV") == "standard":
        unix_socket = f"/cloudsql/{db_connection_name}"
        cnx = pymysql.connect(
            user=db_user, password=db_password, unix_socket=unix_socket, db=db_name
        )
    else:
        host = "127.0.0.1"
        cnx = pymysql.connect(user=db_user, password=db_password, host=host, db=db_name)
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
@jwt_required(refresh=False)
def search():
    search = []
    args = request.args
    nama_destinasi = f"%{args.get('nama_destinasi')}%"
    if os.environ.get("GAE_ENV") == "standard":
        unix_socket = f"/cloudsql/{db_connection_name}"
        cnx = pymysql.connect(
            user=db_user, password=db_password, unix_socket=unix_socket, db=db_name
        )
    else:
        host = "127.0.0.1"
        cnx = pymysql.connect(user=db_user, password=db_password, host=host, db=db_name)
    with cnx.cursor() as cursor:
        cursor.execute('SELECT * FROM destinasi WHERE LOWER(nama_destinasi) LIKE LOWER(%s) ORDER BY nama_destinasi;', (nama_destinasi))
        for row in cursor:
            search.append({'id_destinasi': row[0], 'id_kategori_destinasi': row[1], 'nama_desinasi': row[2], 'deskripsi': row[3], 'pic_destinasi': row[4], 'url_destinasi': row[5]})
        cnx.close()
    return jsonify(search)

#search destinasi
@app.route('/images',methods=["POST", "GET"])
@jwt_required(refresh=False)
def upload():
    if request.method == 'POST':

        img = request.files
        if 'image' not in img:
            return jsonify({
                'message': 'image field must not empty'
            }), 400
        title = ''
        if img['image'] and allowed_file(img['image'].filename):  
            title = str(uuid.uuid4()) + secure_filename(img['image'].filename)
        else:
            return  jsonify({
                'message': 'invalid type format, allowed format (png, jpg, jpeg, gif)'
            }), 400
        encoded = base64.b64encode(img['image'].read())
        

        if os.environ.get("GAE_ENV") == "standard":
            unix_socket = f"/cloudsql/{db_connection_name}"
            cnx = pymysql.connect(
                user=db_user, password=db_password, unix_socket=unix_socket, db=db_name
            )
        else:
            host = "127.0.0.1"
            cnx = pymysql.connect(user=db_user, password=db_password, host=host, db=db_name)
        try:
            with cnx.cursor() as cursor:
                cursor.execute('INSERT INTO pictures(pic,title) VALUES (%s, %s);', (encoded, title))
                cnx.commit()
            cnx.close()
            return jsonify({
                'status':  'success',
                'url': request.base_url+'/'+title
            })
        except Exception as e:
            return jsonify({
                'message': str(e)
            })

@app.route('/images/<string:title>',methods=["GET"])
def get_image(title):
    if request.method == 'GET':
        if title == None:
            return({
                "message": "title need to be specified"
            }), 400

        if os.environ.get("GAE_ENV") == "standard":
            unix_socket = f"/cloudsql/{db_connection_name}"
            cnx = pymysql.connect(
                user=db_user, password=db_password, unix_socket=unix_socket, db=db_name
            )
        else:
            host = "127.0.0.1"
            cnx = pymysql.connect(user=db_user, password=db_password, host=host, db=db_name)
        try:
            with cnx.cursor() as cursor:
                cursor.execute('SELECT pic, title FROM  pictures WHERE title=%s;', (title))
                image = cursor.fetchone()
            cnx.close()
        except Exception as e:
            return jsonify({
                'message': str(e)
            }),400

        binary_data = base64.b64decode(image[0])
        return send_file(io.BytesIO(binary_data), as_attachment=True, download_name=image[1])

@app.route("/GetNull",methods=["POST", "GET"])
def GetNull():
    null = []
    #connect database
    if request.method == 'GET':
        if os.environ.get("GAE_ENV") == "standard":
            unix_socket = f"/cloudsql/{db_connection_name}"
            cnx = pymysql.connect(
                user=db_user, password=db_password, unix_socket=unix_socket, db=db_name
            )
        else:
            host = "127.0.0.1"
            cnx = pymysql.connect(user=db_user, password=db_password, host=host, db=db_name)
        #querying sql
        with cnx.cursor() as cursor:
            cursor.execute('SELECT kategori.id_kategori_user, kategori.id_kategori, user.username_twitter, user.id_user FROM kategori LEFT JOIN user ON kategori.id_kategori_user = user.id_user WHERE kategori.id_kategori is NULL AND user.username_twitter IS NOT NULL;')
            for row in cursor:
                null.append(
                    {
                        'id_kategori_user': row[0],
                        'id_kategori': row[1],
                        'username_twitter':row[2],
                        'user_id':row[3]
                    }
                )
            cnx.commit()
        cnx.close()

        return jsonify(null)
    else:
        return 'Invalid request'

@app.route("/admin/update/user", methods=["PUT"])
@jwt_required(refresh=False)
def update_user():
    if request.method == 'PUT':
        current_user = get_jwt_identity()
        if current_user["status"] != "admin":
            js = {
                'status':'anda tidak memilki akses'
            }
            return jsonify(js),403
        data = request.get_json()
        if os.environ.get("GAE_ENV") == "standard":
            unix_socket = f"/cloudsql/{db_connection_name}"
            cnx = pymysql.connect(
                user=db_user, password=db_password, unix_socket=unix_socket, db=db_name
            )
        else:
            host = "127.0.0.1"
            cnx = pymysql.connect(user=db_user, password=db_password, host=host, db=db_name)
        with cnx.cursor() as cursor:
            cursor.execute('UPDATE kategori SET id_kategori=%s, nama_kategori= %s WHERE id_kategori_user=%s;', (data["kategori"],data["nama_kategori"], data["id_user"]))
            cnx.commit()
            cursor.execute('SELECT id_kategori, id_kategori_user FROM kategori WHERE id_kategori_user=%s;',(data["id_user"]))
            user = cursor.fetchone()
        cnx.close()

        return jsonify(user)
        

    
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
