import pymysql
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
import os

db_user = 'root'
db_password = ''
db_name = 'yourney'
db_connection_name = '127.0.0.1'
    
class UserService:
    def __init__(self,db_user,db_password,db_name,db_connection_name):
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name
        self.db_connection_name = db_connection_name
        
    def check_existing_user(self, username, email):
        cnx = pymysql.connect(host=db_connection_name, user=db_user, 
                          password=db_password, db=db_name)
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
    
    def get_user_by_id(self, id_user):
        cnx = pymysql.connect(host=db_connection_name, user=db_user, 
                          password=db_password, db=db_name)
        with cnx.cursor() as cursor:
            cursor.execute('SELECT user.*, kategori.nama_kategori FROM user LEFT JOIN kategori ON user.id_kategori1 = kategori.id_kategori_user WHERE id_user = %s;',(id_user))
            result = cursor.fetchone()
        cnx.close()
        return result
    
    def user_update_kategori(self,id_user ,id_kategori):
        cnx = pymysql.connect(host=db_connection_name, user=db_user, 
                          password=db_password, db=db_name)
        with cnx.cursor() as cursor:
            cursor.execute('UPDATE user SET id_kategori1=%s WHERE id_user=%s;', (id_kategori, id_user))
            cnx.commit()
        cnx.close()
    
    def user_kategori_null(self):
        null = []
        #connect database
        cnx = pymysql.connect(host=db_connection_name, user=db_user, 
                          password=db_password, db=db_name)
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

        return null
