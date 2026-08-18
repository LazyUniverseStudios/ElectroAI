from db_connection import _ActivePool

async def fetchAllBirthdays():
    """
    Fetches all birthdays from the database.

    Returns:
        list: A list of tuples containing user IDs and their birthdays.
    """
    async with _ActivePool.acquire() as conn:
        async with conn.cursor() as cursor:
            try:
                await cursor.execute("SELECT UserID, Birthday FROM birthdays")
                result = await cursor.fetchall()
                return [(row[0], row[1]) for row in result]
            except Exception as e:
                print(f"Error fetching all birthdays: {e}")
                return []