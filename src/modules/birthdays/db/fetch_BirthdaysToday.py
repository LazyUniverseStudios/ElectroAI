import db_connection

async def fetchTodaysBirthdays(day : str):
    """
    Fetches the user IDs of users whose birthdays are today from the database.

    Args:
        day (str): The current date in the format `1970-MM-DD`.
    
    Returns:
        list: A list of user IDs whose birthdays are today.
    """
    async with db_connection._ActivePool.acquire() as conn:
        async with conn.cursor() as cursor:
            try:
                await cursor.execute("SELECT UserID FROM birthdays WHERE Birthday = %s", (day,))
                result = await cursor.fetchall()
                return [row[0] for row in result]
            except Exception as e:
                print(f"Error fetching today's birthdays: {e}")
                return []