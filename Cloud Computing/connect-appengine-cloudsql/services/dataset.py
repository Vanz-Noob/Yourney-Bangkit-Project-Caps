import pymysql
import os


class DatasetService:
    def __init__(self,db_user,db_password,db_name,db_connection_name):
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name
        self.db_connection_name = db_connection_name
    
    def add_dataset(self,values):
        try:
            if os.environ.get('GAE_ENV') == 'standard':
                unix_socket = '/cloudsql/{}'.format(self.db_connection_name)
                cnx = pymysql.connect(user=self.db_user, password=self.db_password,
                                    unix_socket=unix_socket, db=self.db_name)
            with cnx.cursor() as cursor:
                cursor.executemany('INSERT INTO dataset(created_at,author,tweet,kategori) VALUES (%s,%s,%s,%s) ;',values)
                cnx.commit()
            cnx.close()

            return
        except Exception as e:
            print(str(e))

    def get_dataset_by_kategori(self):
        if os.environ.get('GAE_ENV') == 'standard':
            unix_socket = '/cloudsql/{}'.format(self.db_connection_name)
            cnx = pymysql.connect(user=self.db_user, password=self.db_password,
                                unix_socket=unix_socket, db=self.db_name)
        with cnx.cursor() as cursor:
            cursor.execute('SELECT * FROM dataset;')
            result = cursor.fetchone()
        cnx.close()
        return result
