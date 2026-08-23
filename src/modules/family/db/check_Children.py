import db_connection

async def check_children(user_id):
    async with db_connection._ActivePool.acquire() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute("""
                SELECT Child1ID, Child2ID, Child3ID, Child4ID, Child5ID, Child6ID
                FROM Family 
                WHERE UserID = %s""", 
                (user_id,)
            )

            result = await cursor.fetchone()

            children = list(result) if result else []

            return children