import db_connection

async def check_parent(user_id):
    async with db_connection._ActivePool.acquire() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute("SELECT ParentID FROM Family WHERE UserID = %s", (user_id,))
            result = await cursor.fetchone()

            if result is not None:
                parent_id = result[0]
                if parent_id is not None:
                    return True, parent_id
                else:
                    return False, None
            else:
                return False, None
