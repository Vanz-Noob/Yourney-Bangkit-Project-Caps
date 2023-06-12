import pymysql
import os


db_user = 'root'
db_password = ''
db_name = 'yourney'
db_connection_name = '127.0.0.1'

class DatasetService:
    def __init__(self,db_user,db_password,db_name,db_connection_name):
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name
        self.db_connection_name = db_connection_name
    def add_dataset(self,values):
        try:
            cnx = pymysql.connect(host=db_connection_name, user=db_user, 
                          password=db_password, db=db_name)
            with cnx.cursor() as cursor:
                cursor.executemany('INSERT INTO dataset(create_time,author,tweet,kategori) VALUES (%s,%s,%s,%s) ;',values)
                cnx.commit()
            cnx.close()

            return
        except Exception as e:
            print(str(e))

    def get_dataset_by_kategori(self):
        cnx = pymysql.connect(host=db_connection_name, user=db_user, 
                          password=db_password, db=db_name)
        with cnx.cursor() as cursor:
            cursor.execute('SELECT * FROM dataset;')
            result = cursor.fetchone()
        cnx.close()
        return result
