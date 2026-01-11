import mysql.connector
import os
import dotenv

dotenv.load_dotenv()
DB_ADDRESS = os.getenv("DB_ADDRESS")
DB_PORT = int(os.getenv("DB_PORT"))
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def DB_GetConnection():
    return mysql.connector.connect(
        host=DB_ADDRESS,
        port = DB_PORT,
        username = DB_USERNAME,
        password = DB_PASSWORD,
        database = DB_NAME
        )
