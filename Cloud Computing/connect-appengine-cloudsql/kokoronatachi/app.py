from crypt import methods
import datetime
import logging
import os

from flask import Flask, request, Response

import sqlalchemy

# bisa pilih salah satu
from connect_connector import connect_with_connector
from connect_unix import connect_unix_socket

app = Flask(__name__)

logger = logging.getLogger()

def init_connection_pool() -> sqlalchemy.engine.base.Engine:
     # use a Unix socket when INSTANCE_UNIX_SOCKET (e.g. /cloudsql/project:region:instance) is defined
    if os.environ.get("INSTANCE_UNIX_SOCKET"):
        return connect_unix_socket()
    # use the connector when INSTANCE_CONNECTION_NAME (e.g. project:region:instance) is defined
    if os.environ.get("INSTANCE_CONNECTION_NAME"):
        return connect_with_connector()

    raise ValueError(
        "Missing database connection type. Please define one of INSTANCE_HOST, INSTANCE_UNIX_SOCKET, or INSTANCE_CONNECTION_NAME"
    )
# membuat db jika belum ada
def migrate_db(db: sqlalchemy.engine.base.Engine) -> None:
    with db.connect() as conn:
        conn.execute(
            "CREATE DATABASE IF NOT EXIST yourney"
        )
db = None
@app.before_request
def init_db() -> sqlalchemy.engine.base.Engine:
    global db
    db = init_connection_pool()
    migrate_db(db)
    
@app.route('/', methods=["GET"])
def hello():
    return "Hello, World This Is Yourney!"