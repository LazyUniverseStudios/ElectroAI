import aiomysql as mysqlconnector
from .DBConnection import DB_GetConnection

async def CreateUserIfNotExists(user_id: int):
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    await cursor.execute("SELECT * FROM users WHERE UserID = %s", (user_id,))
    result = await cursor.fetchone()
    if not result:
        await cursor.execute("INSERT INTO users (UserID) VALUES (%s)", (user_id,))
        await cursor.execute("INSERT INTO Leveling (UserID) VALUES (%s)", (user_id,))
        await cursor.execute("INSERT INTO Economy (UserID) VALUES (%s)", (user_id,))
        await conn.commit()
    await cursor.close()
    conn.close()

async def DropUser(user_id: int):
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    await cursor.execute("SELECT * FROM users WHERE UserID = %s", (user_id,))
    result = await cursor.fetchone()
    if result:
        await cursor.execute("DELETE FROM users WHERE UserID = %s", (user_id,))
        await conn.commit()
    await cursor.close()
    conn.close()