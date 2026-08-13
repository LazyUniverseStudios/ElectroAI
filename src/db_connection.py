import aiomysql as amysql
import os
import config

DB_ADDRESS = os.getenv("DB_ADDRESS")
DB_PORT = int(os.getenv("DB_PORT"))
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

_ActivePool = None

async def createPool():
    """
    Creates a connection pool for the MySQL database using aiomysql. This function ensures that only one pool is created and reused throughout the application.
    Returns:
        aiomysql.Pool: A connection pool for the MySQL database.
    Raises:
        Exception: If there is an error creating the connection pool.
    """
    global _ActivePool
    if _ActivePool is not None:
        return _ActivePool
    else:
        try:
            _ActivePool =  await amysql.create_pool(
                host=DB_ADDRESS,
                port=DB_PORT,
                user=DB_USERNAME,
                password=DB_PASSWORD,
                db=DB_NAME,

                minsize=config.POOL_MIN_SIZE,
                maxsize=config.POOL_MAX_SIZE
            )
            return _ActivePool
        except Exception as e:
            print(f"Error creating database connection pool: {e}")
            raise e
