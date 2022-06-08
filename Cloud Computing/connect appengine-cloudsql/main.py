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

@app.route("/", methods=["GET"])
def hello():
    return "Hello, World This Is Yourney!"
    
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
#sudah okay
@app.route("/login",methods=["POST", "GET"])
def login():
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
        cursor.execute('SELECT * FROM user WHERE username = %s AND password = %s;', (username, password))
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
            "password": password,
            "code": "sukses",
        }
        
    return jsonify(js)

#register
#sudah okay
@app.route("/register",methods=["POST", "GET"])
def register():
    request_data = request.get_json()
    username = request_data['username']
    password = request_data['password']
        
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
        cursor.execute('INSERT INTO user (username, password) VALUES (%s, %s);', (username, password))
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
            "password": password,
            "code": "sukses",
        }
    return jsonify(js)



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
