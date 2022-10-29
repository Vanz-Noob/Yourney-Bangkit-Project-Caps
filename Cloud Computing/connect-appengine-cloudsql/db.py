from calendar import c
from email.message import Message
from msilib.schema import Binary
import os
import pymysql

from flask import Flask, jsonify, request

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')


def open_conn():
    unix_socket = '/cloudsql/{}'.format(db_connection_name)
    try:
        if os.environ.get('GAE_ENV') == 'standard':
            conn = pymysql.connect(user=db_user,
                                   password=db_password,
                                   unix_socket=unix_socket,
                                   db=db_name,
                                   cursorclass=pymysql.cursors.DictCursor
                                   )
    except pymysql.MySQLError as e:
        return e
    return conn

def get_destinasi():
    conn = open_conn()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM destinasi;')
        destinasi = cursor.fetchall()
        if result > 0:
            got_destinasi = jsonify(destinasi)
        else:
            got_destinasi = jsonify({"message" : "No destinasi in DB"})
        return got_destinasi

def get_kategori():
    conn = open_conn()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM kategori;')
        kategori = cursor.fetchall()
        if result > 0:
            got_kategori = jsonify(kategori)
        else:
            got_kategori = jsonify({"message" : "No kategori in DB"})
        return got_kategori
    
def get_db():
    conn = open_conn()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM user;')
        user = cursor.fetchall()
        if result > 0:
            got_users = jsonify(user)
        else:
            got_users = jsonify({"message" : "No user in DB"})
        return got_users

# # TODO
# # masih bingung dalam memasukan blob bentuk TEXT
# def InsertBlob(FilePath):
#     with open(FilePath, "rb") as File:
#         BinaryData = File.read()
    
# def post_destinasi(destinasi):
#     conn = open_conn()
#     with conn.cursor() as cursor:
#         cursor.execute('INSERT INTO destinasi (nama_destinasi) VALUES (%s);', 
#                        (destinasi["nama_destinasi"]))
#         conn.commit()
#         conn.close()


def post_kategori(kategori):
    conn = open_conn()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO kategori (nama_kategori) VALUES (%s);', 
                       (kategori["nama_kategori"]))
        conn.commit()
        conn.close()
        