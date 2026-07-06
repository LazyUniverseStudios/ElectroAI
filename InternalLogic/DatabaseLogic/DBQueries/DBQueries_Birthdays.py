from InternalLogic.DatabaseLogic.DBConnection import DB_GetConnection

async def SetUserBirthday(user_id: int, birthday: str):
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    try:
        await cursor.execute("INSERT INTO birthdays (UserID, Birthday) VALUES (%s, %s) ON DUPLICATE KEY UPDATE Birthday = %s", (user_id, birthday, birthday))
        await conn.commit()
    except Exception as e:
        print(f"Error setting birthday for user {user_id}: {e}")
        await conn.rollback()
    finally:
        await cursor.close()
        conn.close()