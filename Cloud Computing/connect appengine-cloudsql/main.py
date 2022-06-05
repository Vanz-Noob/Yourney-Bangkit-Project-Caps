import datetime
import logging
import os
from typing import Dict

from flask import Flask, render_template, request, Response

import sqlalchemy

from connect_connector import connect_with_connector
from connect_tcp import connect_tcp_socket
from connect_unix import connect_unix_socket

app = Flask(__name__)

logger = logging.getLogger()

def init_connection_pool() -> sqlalchemy.engine.base.Engine:
    # use a TCP socket when INSTANCE_HOST (e.g. 127.0.0.1) is defined
    if os.environ.get("INSTANCE_HOST"):
        return connect_tcp_socket()

    # use a Unix socket when INSTANCE_UNIX_SOCKET (e.g. /cloudsql/project:region:instance) is defined
    if os.environ.get("INSTANCE_UNIX_SOCKET"):
        return connect_unix_socket()

    # use the connector when INSTANCE_CONNECTION_NAME (e.g. project:region:instance) is defined
    if os.environ.get("INSTANCE_CONNECTION_NAME"):
        return connect_with_connector()

    raise ValueError(
        "Missing database connection type. Please define one of INSTANCE_HOST, INSTANCE_UNIX_SOCKET, or INSTANCE_CONNECTION_NAME"
    )
db = None

@app.before_first_request
def init_db() -> sqlalchemy.engine.base.Engine:
    global db
    db = init_connection_pool()
    migrate_db(db)
    
def get_index_context(db: sqlalchemy.engine.base.Engine) -> Dict:
    demo_txt = []

    with db.connect() as conn:
        # Execute the query and fetch all results
        recent_demo = conn.execute(
            "SELECT demo_txt FROM demo_tbl"
        ).fetchall()
        # Convert the results into a list of dicts representing votes
        for row in recent_demo:
            demo.append({"demo_txt": row[0]})

                # stmt = sqlalchemy.text(
                #     "SELECT COUNT(demo_id) FROM demo WHERE demo_txt=:demo_txt"
                # )
                # # Count number of votes for tabs
                # tab_result = conn.execute(stmt, candidate="TABS").fetchone()
                # tab_count = tab_result[0]
                # # Count number of votes for spaces
                # space_result = conn.execute(stmt, candidate="SPACES").fetchone()
                # space_count = space_result[0]

    return (recent_demo)
    
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)