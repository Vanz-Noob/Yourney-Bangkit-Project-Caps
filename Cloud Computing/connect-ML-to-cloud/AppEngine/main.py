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
from helper.twitter import average_data
from helper.user import UserService
import pymysql

db_host = os.environ["INSTANCE_HOST"]  # e.g. '127.0.0.1' ('172.17.0.1' if deployed to GAE Flex)
db_user = os.environ["DB_USER"]  # e.g. 'my-db-user'
db_pass = os.environ["DB_PASS"]  # e.g. 'my-db-password'
db_name = os.environ["DB_NAME"]  # e.g. 'my-database'
db_port = os.environ["DB_PORT"]  # e.g. 3306


app = Flask(__name__)
user_service = UserService(db_user,db_password,db_name,db_connection_name, db_host)

@app.route("/", methods=["GET"])
def hello():
    return "Hello, World This Is Yourney!"

@app.route("/GetNull",methods=["POST", "GET"])
def GetNull():
    null = []
    #connect database
    if request.method == 'GET':
        if os.environ.get('GAE_ENV') == 'standard':
            unix_socket = '/cloudsql/{}'.format(db_connection_name)
            cnx = pymysql.connect(user=db_user, password=db_password,
                                unix_socket=unix_socket, db=db_name)
        else:
            host = db_host
            cnx = pymysql.connect(user=db_user, password=db_password,
                                host=host, db=db_name)
        #querying sql
        with cnx.cursor() as cursor:
            cursor.execute('SELECT kategori.id_kategori_user, kategori.id_kategori, user.username, user.id_user FROM kategori LEFT JOIN user ON kategori.id_kategori_user = user.id_user WHERE id_kategori is NULL;')
            for row in cursor:
                null.append(
                    {
                        'id_kategori_user': row[0],
                        'id_kategori': row[1],
                        'username':row[2],
                        'user_id':row[3]
                    }
                )
            cnx.commit()
        cnx.close()

        for user in null:
            id_kategori = average_data(user['username'])
            user_service.user_update_kategori(id_kategori)
            user['id_kategori'] = id_kategori


        return jsonify(null)
    else:
        return 'Invalid request'

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
