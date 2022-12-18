import pymysql
import os


class UserService:
    def __init__(self,db_user,db_password,db_name,db_connection_name):
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name
        self.db_connection_name = db_connection_name
    
    def user_update_kategori(self,id_user ,id_kategori):
        if os.environ.get('GAE_ENV') == 'standard':
            unix_socket = '/cloudsql/{}'.format(self.db_connection_name)
            cnx = pymysql.connect(user=self.db_user, password=self.db_password,
                                unix_socket=unix_socket, db=self.db_name)
        else:
            host = '127.0.0.1'
            cnx = pymysql.connect(user=self.db_user, password=self.db_password,
                                host=host, db=self.db_name)
        with cnx.cursor() as cursor:
            cursor.execute('UPDATE user SET id_kategori1=%s WHERE id_user=%s;', (id_kategori, id_user))
            cnx.commit()
        cnx.close()
