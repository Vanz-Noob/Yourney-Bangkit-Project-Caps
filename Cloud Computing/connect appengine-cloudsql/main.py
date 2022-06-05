# [START gae_python37_cloudsql_mysql]
import os

from flask import Flask,jsonify,request
import pymysql

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

app = Flask(__name__)

#test server
@app.route('/')
def hello():
    return 'Hello World!'

# route login
@app.route('/auth/login')
def login():
    username = str(request.args.get('username'))
    password = str(request.args.get('password'))
    #connect to cloud sql
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
        cursor.execute('SELECT * FROM USER WHERE username = %s', username)
        result = cursor.fetchone()
        if result is not None:
            if result[1] == password:
                js={
                    "code":"Login sukses";
                }
            else:
                js={
                    code:"Login gagal";
                }
        else:
            js={
                code:"Login gagal";
            }
        return jsonify(js)
    cnx.close()
    
# route register
@app.route('/auth/register')
def register():
    username = str(request.args.get('username'))
    password = str(request.args.get('password'))
    #connect to cloud sql
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
        cursor.execute("INSERT INTO USER (username, password) VALUES (%s, %s)", (username, password))
        result = cursor.fetchone()
        cnx.commit()
    cnx.close()
    with cnx.cursor() as cursor:
        cursor.execute('SELECT * FROM USER WHERE username = %s and password =%s', username, password)
        result = cursor.fetchone()
        if result is not None:
            if result[1] == password:
                js={
                    "code":"Login sukses";
                }
            else:
                js={
                    code:"Login gagal";
                }
        else:
            js={
                code:"Login gagal";
            }
        return jsonify(js)
    cnx.close()
            
@app.route('/db')
def main():
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
        #query pending
        cursor.execute('SELECT demo_db FROM demo_tbl;)
        result = cursor.fetchall()
        current_msg = result[0][0]
    cnx.close()

    return str(current_msg)
# [END gae_python37_cloudsql_mysql]


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)