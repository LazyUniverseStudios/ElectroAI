import db_connection

async def fetchUserBirthday(user_id):
    """
    Fetches the birthday of a user from the database.

    Args:
        user_id (int): The ID of the user whose birthday is being fetched.
    
    Returns:
        str or None: The birthday in the format `1970-MM-DD` if found, otherwise None.
    """
    async with db_connection._ActivePool.acquire() as conn:
        async with conn.cursor() as cursor:
            try:
                await cursor.execute("SELECT Birthday FROM birthdays WHERE UserID = %s", (user_id,))
                result = await cursor.fetchone()
                return result[0] if result else None
            except Exception as e:
                print(f"Error fetching user birthday: {e}")
                return None
