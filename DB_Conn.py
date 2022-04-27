import os
import contextlib
import mysql.connector

@contextlib.contextmanager
def get_mysql_conn():
    config = {
        'user': 'root',
        'password': 'xpto13',
        'host': 'localhost',
        'database': 'COB',
        'raise_on_warnings': True}

    conn = mysql.connector.connect(**config)
    try:
        yield conn
    finally:
        conn.close()