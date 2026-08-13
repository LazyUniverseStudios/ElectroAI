from db_connection import _ActivePool

async def setUserBirthday(user_id: int, birthday: str):
    """
    Sets the birthday for a user in the database.

    Args:
        user_id (int): The ID of the user whose birthday is being set.
        birthday (str): The birthday in the format `1970-MM-DD`.
    
    Returns:
        bool: True if the birthday was set successfully, False otherwise.
    """

    async with _ActivePool.acquire() as conn:
        async with conn.cursor() as cursor:
            try:
                await cursor.execute("""
                                    UPDATE Birthdays
                                    SET Birthday = %s
                                    WHERE UserID = %s
                                    """, (birthday, user_id))
                await conn.commit()
                return True
            except Exception as e:
                print(f"Error setting user birthday: {e}")
                await conn.rollback()
                return False