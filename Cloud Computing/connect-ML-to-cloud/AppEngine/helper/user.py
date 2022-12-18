import pymysql

class UserService:
    def __init__(self,db_user,db_password,db_name,db_host):
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name
        self.db_host = db_host
    
    def user_update_kategori(self,id_user ,id_kategori):
    #connect database
        cnx = pymysql.connect(user=self.db_user, password=self.db_password,
                                host=self.db_host, db=self.db_name)
        with cnx.cursor() as cursor:
            cursor.execute('UPDATE user SET id_kategori1=%s WHERE id_user=%s;', (id_kategori, id_user))
            cnx.commit()
        cnx.close()
