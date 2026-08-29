import db_connection

async def check_spouse(user_id):
    async with db_connection._ActivePool.acquire() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute("""
                SELECT Partner1ID, Partner2ID, Partner3ID, Partner4ID
                FROM Family 
                WHERE UserID = %s""", 
                (user_id,)
            )

            result = await cursor.fetchone()
            await connection.commit()

            spouses = [result[0], result[1], result[2], result[3]] if result else []

            return spouses