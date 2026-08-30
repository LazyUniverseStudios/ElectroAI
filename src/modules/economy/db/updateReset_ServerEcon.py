import db_connection

async def UpdateServerEconomy_Reset():
    async with db_connection._ActivePool.acquire() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute("""
                UPDATE Economy
                SET Coins = 0, DailyRewardNextUse = NULL, WeeklyRewardNextUse = NULL, MonthlyRewardNextUse = NULL
            """)
            await connection.commit()