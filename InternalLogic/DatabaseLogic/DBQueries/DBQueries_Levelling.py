from InternalLogic.DatabaseLogic.DBConnection import DB_GetConnection

async def FetchUserLevel(user_id: int):
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    try:
        await cursor.execute("SELECT Level FROM leveling WHERE UserID = %s", (user_id,))
        result = await cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error fetching user level for user {user_id}: {e}")
        return None
    finally:
        await cursor.close()
        conn.close()

async def UpdateUserLeveling_Reset(user_id: int):
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    try:
        await cursor.execute("UPDATE leveling SET Level = 0 WHERE UserID = %s", (user_id,))
        await cursor.execute("UPDATE leveling SET XP = 0 WHERE UserID = %s", (user_id,))
        await cursor.execute("UPDATE leveling SET XPForNextLevel = 100 WHERE UserID = %s", (user_id,))
        await cursor.execute("UPDATE leveling SET TotalXP = 0 WHERE UserID = %s", (user_id,))
        await conn.commit()
    except Exception as e:
        print(f"Error resetting user leveling for user {user_id}: {e}")
        await conn.rollback()
    finally:
        await cursor.close()
        conn.close()

async def UpdateUserXP_Add(user_id: int, amount: int):
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    try:
        await cursor.execute("UPDATE leveling SET XP = XP + %s WHERE UserID = %s", (amount, user_id))
        await cursor.execute("UPDATE leveling SET TotalXP = TotalXP + %s WHERE UserID = %s", (amount, user_id))
        await conn.commit()
    except Exception as e:
        print(f"Error updating user XP for user {user_id}: {e}")
        await conn.rollback()
    finally:
        await cursor.close()
        conn.close()

async def UpdateUserXP_Subtract(user_id: int, amount: int):
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    try:
        await cursor.execute("UPDATE leveling SET XP = XP - %s WHERE UserID = %s AND XP >= %s", (amount, user_id, amount))
        await cursor.execute("UPDATE leveling SET TotalXP = TotalXP - %s WHERE UserID = %s AND TotalXP >= %s", (amount, user_id, amount))
        await conn.commit()
        result = cursor.rowcount
    except Exception as e:
        print(f"Error updating user XP for user {user_id}: {e}")
        await conn.rollback()
        result = 0
    finally:
        await cursor.close()
        conn.close()
    return result

async def UpdateUserXP_Set(user_id: int, xp: int):
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    try:
        await cursor.execute("UPDATE leveling SET XP = %s WHERE UserID = %s", (xp, user_id))
        await conn.commit()
    except Exception as e:
        print(f"Error setting user XP for user {user_id}: {e}")
        await conn.rollback()
    finally:
        await cursor.close()
        conn.close()