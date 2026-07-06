from InternalLogic.DatabaseLogic.DBConnection import DB_GetConnection

async def FetchUserLevelingData(user_id: int):
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    try:
        await cursor.execute("SELECT Level, XP, XPForNextLevel, TotalXP FROM leveling WHERE UserID = %s", (user_id,))
        result = await cursor.fetchone()
        if result:
            return {
                "Level": result[0],
                "XP": result[1],
                "XPForNextLevel": result[2],
                "TotalXP": result[3]
            }
        else:
            return None
    except Exception as e:
        print(f"Error fetching user leveling data for user {user_id}: {e}")
        return None
    finally:
        await cursor.close()
        conn.close()

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

async def FetchUserXP(user_id: int):
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    try:
        await cursor.execute("SELECT XP FROM leveling WHERE UserID = %s", (user_id,))
        result = await cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error fetching user XP for user {user_id}: {e}")
        return None
    finally:        
        await cursor.close()
        conn.close()

async def FetchUserXPNextLevel(user_id: int):
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    try:
        await cursor.execute("SELECT XPForNextLevel FROM leveling WHERE UserID = %s", (user_id,))
        result = await cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error fetching user XP for next level for user {user_id}: {e}")
        return None
    finally:
        await cursor.close()
        conn.close()

async def FetchUserTotalXP(user_id: int):
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    try:
        await cursor.execute("SELECT TotalXP FROM leveling WHERE UserID = %s", (user_id,))
        result = await cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error fetching user total XP for user {user_id}: {e}")
        return None
    finally:
        await cursor.close()
        conn.close()

async def FetchServerLevelingData():
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    try:
        await cursor.execute("SELECT UserID, Level, XP, XPForNextLevel, TotalXP FROM leveling")
        result = await cursor.fetchall()
        return [{
            "UserID": row[0],
            "Level": row[1],
            "XP": row[2],
            "XPForNextLevel": row[3],
            "TotalXP": row[4]
        } for row in result]
    except Exception as e:
        print(f"Error fetching server leveling data: {e}")
        return None
    finally:
        await cursor.close()
        conn.close()

async def FetchServerLevel():
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    try:
        await cursor.execute("SELECT UserID, Level FROM leveling")
        result = await cursor.fetchall()
        return [{
            "UserID": row[0],
            "Level": row[1]
        } for row in result]
    except Exception as e:
        print(f"Error fetching server level data: {e}")
        return None
    finally:        
        await cursor.close()
        conn.close()

async def FetchServerXP():
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    try:
        await cursor.execute("SELECT UserID, XP FROM leveling")
        result = await cursor.fetchall()
        return [{
            "UserID": row[0],
            "XP": row[1]
        } for row in result]
    except Exception as e:
        print(f"Error fetching server XP data: {e}")
        return None
    finally:
        await cursor.close()
        conn.close()

async def FetchServerTotalXP():
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    try:
        await cursor.execute("SELECT UserID, TotalXP FROM leveling")
        result = await cursor.fetchall()
        return [{
            "UserID": row[0],
            "TotalXP": row[1]
        } for row in result]
    except Exception as e:
        print(f"Error fetching server total XP data: {e}")
        return None
    finally:
        await cursor.close()
        conn.close()    

async def FetchServerXPNextLevel():
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    try:
        await cursor.execute("SELECT UserID, XPForNextLevel FROM leveling")
        result = await cursor.fetchall()
        return [{
            "UserID": row[0],
            "XPForNextLevel": row[1]
        } for row in result]
    except Exception as e:
        print(f"Error fetching server XP for next level data: {e}")
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