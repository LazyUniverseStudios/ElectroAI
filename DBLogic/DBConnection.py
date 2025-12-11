import mysql.connector

from config import DB_ADDRESS, DB_NAME, DB_PASSWORD, DB_USERNAME, DB_PORT

def DB_GetConnection():
    return mysql.connector.connect(
        host=DB_ADDRESS,
        port = DB_PORT,
        username = DB_USERNAME,
        password = DB_PASSWORD,
        database = DB_NAME
        )
