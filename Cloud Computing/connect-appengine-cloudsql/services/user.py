import pymysql
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
import os


class UserService:
    def __init__(self,db_user,db_password,db_name,db_connection_name):
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name
        self.db_connection_name = db_connection_name
    
    def check_existing_user(self, username, email):
        if os.environ.get('GAE_ENV') == 'standard':
            unix_socket = '/cloudsql/{}'.format(self.db_connection_name)
            cnx = pymysql.connect(user=self.db_user, password=self.db_password,
                                unix_socket=unix_socket, db=self.db_name)
        else:
            host = '127.0.0.1'
            cnx = pymysql.connect(user=self.db_user, password=self.db_password,
                                host=host, db=self.db_name)
        with cnx.cursor() as cursor:
            cursor.execute('SELECT id_user FROM user WHERE LOWER(username) = LOWER(%s) OR LOWER(email) = LOWER(%s);',(username, email))
            result = cursor.fetchone()
        cnx.close()

        return result
    
    @jwt_required(refresh=True)
    def refresh(self):
        try:
            user = get_jwt_identity()
            new_token = create_access_token(identity=user, fresh=False)
            return jsonify({
                "access": new_token
             }),201

        except Exception as e:
            print(e)