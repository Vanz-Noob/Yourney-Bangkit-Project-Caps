# Store this code in 'app.py' file

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import pymysql
from passlib.hash import sha256_crypt

db_user = 'root'
db_password = ''
db_name = 'yourney'
db_connection_name = '127.0.0.1'

app = Flask(__name__)

mysql = MySQL(app)

@app.route('/')
@app.route("/login",methods=["POST", "GET"])
def login():
    try:
        request_data = request.get_json()
        username = request_data['username']
        password = request_data['password']
        #connect database
        cnx = pymysql.connect(host=db_connection_name, user=db_user, 
                          password=db_password, db=db_name)
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
        # expires = timedelta(days=1)
        # expires_refresh = timedelta(days=3)
        # identity = {
        #     'id_user': user[0],
        #     'username': user[5],
        #     'status':user[9]
        # }

        # access_token = create_access_token(identity=identity, fresh=True, expires_delta=expires)
        # refresh_token = create_refresh_token(identity=identity, expires_delta=expires_refresh)
        return jsonify(
            {
                'status': 'success',
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

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('login'))

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
        

        cnx = pymysql.connect(user=db_user, password=db_password,
                                host=db_connection_name, db=db_name)
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
        # exist = user_service.check_existing_user(username, email)

        # if exist:
        #     return jsonify(
        #         {
        #             'message': 'user already exist'
        #         }
        #     ), 400

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

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)