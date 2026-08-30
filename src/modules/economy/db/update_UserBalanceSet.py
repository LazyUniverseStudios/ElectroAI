import db_connection

async def updateUserBalance_Set(user_id, amount):
    async with db_connection._ActivePool.acquire() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute("""
                UPDATE Economy
                SET Coins = %s
                WHERE UserID = %s""",
                (amount, user_id)
            )
            await connection.commit()