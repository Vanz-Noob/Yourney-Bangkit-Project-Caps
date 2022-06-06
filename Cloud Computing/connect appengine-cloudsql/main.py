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

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"
    
@app.route('/db')
def db():
    # When deployed to App Engine, the `GAE_ENV` environment variable will be
    # set to `standard`
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'
        cnx = pymysql.connect(user=db_user, password=db_password,
                              host=host, db=db_name)

    with cnx.cursor() as cursor:
        cursor.execute('SELECT * FROM user;')
        result = cursor.fetchall()
        # teks = result[0][1]
    cnx.close()
    if result == 0:
        js = {
            "code" : "gagal",
        }
    else:
        js = {
            "code" : "sukses",
            "idUser" : result[0][0],
            "username" : result[0][1],
            "password" : result[0][2],
        }
    return jsonify(js)
    # return str(teks)
    
#login
@app.route('/login', methods=["POST"])
def login():
    # prm_username = str(request.args.get("username"))
    # prm_password = str(request.args.get("password"))
    prm_username = request.args.get("username")
    prm_password = request.args.get("password")
    # prm_username = request.form['username']
    # prm_password = request.form['password']
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                                unix_socket=unix_socket, db=db_name)
    else:
        host = '127.0.0.1'
        cnx = pymysql.connect(user=db_user, password=db_password,
                                host=host, db=db_name)
    with cnx.cursor() as cursor:
        cursor.execute("select * from user where username='"+prm_username+"' and password='"+prm_password+"';")
        # cursor.execute("SELECT * FROM user WHERE username='"+prm_username+"' AND password='"+prm_password+"';")
        cursor.execute("SELECT * FROM user WHERE username = %s AND password = %s",(prm_username, prm_password))
        result = cursor.fetchall()
    cnx.close()

    if result == 0:
        js = {
            "code" : "gagal",
        }
    else:
        js = {
            "code" : "sukses",
            "msg" : "Selamat datang",
        }
    return jsonify(js)

#register
@app.route("/register", methods=["POST", "GET"])
def register():
    # prm_username = request.args.get("username")
    # prm_password = request.args.get("password")
    prm_username = request.form.get['username']
    prm_password = request.form.get['password']
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    else:
        host = '127.0.0.1'
        cnx = pymysql.connect(user=db_user, password=db_password,
                              host=host, db=db_name)
    
    with cnx.cursor() as cursor:
        # cursor.execute("insert into user(username, password) values ('"+prm_username+"', '"+prm_password+"');")
        cursor.execute("INSERT INTO user(username, password) VALUES ('"+prm_username+"', '"+prm_password+"');")
        # cursor.execute("INSERT INTO user(username, password) VALUES (%s, %s)", (prm_username, prm_password))
        result = cursor.fetchone()
        cnx.commit()
    cnx.close()

    with cnx.cursor() as cursor:
        # cursor.execute("select * from user where username='"+prm_username+"' and password='"+prm_password+"';")
        cursor.execute("SELECT * FROM user WHERE username='"+prm_username+"' and password='"+prm_password+"';")
        # cursor.execute("SELECT * FROM user WHERE username = %s AND password = %s",(prm_username, prm_password))
        result = cursor.fetchall()
    cnx.close()

    if result == 0:
        js = {
            "code" : "gagal",
        }
    else:
        js = {
            "code" : "sukses",
            "msg" : "Selamat datang",
        }
    return jsonify(js)

@app.route('/output')
def output():
    pass
# [END gae_python3_cloudsql_mysql]
# [END gae_python38_cloudsql_mysql]


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
