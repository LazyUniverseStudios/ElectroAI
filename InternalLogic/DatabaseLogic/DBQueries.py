import aiomysql as mysqlconnector
from .DBConnection import DB_GetConnection

async def CreateUserIfNotExists(user_id: int):
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    await cursor.execute("SELECT * FROM users WHERE UserID = %s", (user_id,))
    result = await cursor.fetchone()
    if not result:
        await cursor.execute("INSERT INTO users (UserID) VALUES (%s)", (user_id,))
        await cursor.execute("INSERT INTO leveling (UserID) VALUES (%s)", (user_id,))
        await cursor.execute("INSERT INTO economy (UserID) VALUES (%s)", (user_id,))
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

async def FetchUserBalance(user_id: int):
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    await cursor.execute("SELECT Coins FROM economy WHERE UserID = %s", (user_id,))
    result = await cursor.fetchone()
    await cursor.close()
    conn.close()
    return result[0] if result else None

async def UpdateUserBalance_Add(user_id: int, amount: int):
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    await cursor.execute("UPDATE economy SET Coins = Coins + %s WHERE UserID = %s", (amount, user_id))
    await conn.commit()
    await cursor.close()
    conn.close()

async def UpdateUserBalance_Subtract(user_id: int, amount: int):
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    await cursor.execute("UPDATE economy SET Coins = Coins - %s WHERE UserID = %s AND Coins >= %s", (amount, user_id, amount))
    await conn.commit()
    result = cursor.rowcount
    await cursor.close()
    conn.close()
    return result

async def UpdateUserBalance_Set(user_id: int, amount: int):
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    await cursor.execute("UPDATE economy SET Coins = %s WHERE UserID = %s", (amount, user_id))
    await conn.commit()
    await cursor.close()
    conn.close()