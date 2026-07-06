import aiomysql as mysqlconnector
import os
import dotenv

dotenv.load_dotenv(dotenv_path="../../.env")
DB_ADDRESS = os.getenv("DB_ADDRESS")
DB_PORT = int(os.getenv("DB_PORT"))
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

async def DB_GetConnection():
    return await mysqlconnector.connect(
        host=DB_ADDRESS,
        port = DB_PORT,
        user = DB_USERNAME,
        password = DB_PASSWORD,
        db = DB_NAME
        )
