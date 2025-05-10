# db_config.py

import mysql.connector
from mysql.connector import errorcode

# 1) MySQL connection settings—you already tested these in setup_db.py
DB_CONFIG = {
    'user':     'root',
    'password': 'password',
    'host':     '127.0.0.1',        # or 'localhost'
    'port':     3306,
    'database': 'Jellies',        # directly connect to the Jellies DB
    'autocommit': False           # we'll commit manually
}

def get_connection():
    """
    Returns a new MySQL connection using DB_CONFIG.
    Caller is responsible for closing the connection.
    """
    try:
        cnx = mysql.connector.connect(**DB_CONFIG)
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            raise RuntimeError("Access denied: check your DB credentials") from err
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            raise RuntimeError("Database does not exist. Run setup_db.py first.") from err
        else:
            raise

def close_connection(cnx):
    """Closes the given MySQL connection, if open."""
    try:
        if cnx and cnx.is_connected():
            cnx.close()
    except mysql.connector.Error:
        pass
