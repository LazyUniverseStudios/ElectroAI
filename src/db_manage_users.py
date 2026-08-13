from db_connection import _ActivePool

async def CreateUserIfNotExists(user_id: int):
    """
    Ensures a user exists across all ElectroAI tables atomically.

    Args:
        user_id (int): The ID of the user to ensure exists in the database.
    """

    async with _ActivePool.acquire() as conn:
        async with conn.cursor() as cursor:
            try:
                await cursor.execute(
                    f"INSERT IGNORE INTO `ElectroAI`.`Users` (`UserID`) VALUES (%s)",
                    (user_id,),
                )
                await conn.commit()
            except Exception as e:
                await conn.rollback()
                print(f"Error ensuring record existence for user {user_id}: {e}")

async def DropUser(user_id: int):
    """
    Deletes a user from all ElectroAI tables atomically.
    """

    async with _ActivePool.acquire() as conn:
        async with conn.cursor() as cursor:
            try:
                await cursor.execute("SELECT * FROM users WHERE UserID = %s", (user_id,))
                result = await cursor.fetchone()
                if result:
                    await cursor.execute("DELETE FROM Users WHERE UserID = %s", (user_id,))
                    await conn.commit()
                else:
                    print(f"User {user_id} does not exist in the Users table.")
            except Exception as e:
                await conn.rollback()
                print(f"Error deleting user {user_id}: {e}")

async def BackfillUsers():
    """
    Backfills users across all ElectroAI tables after an update.
    """

    dependent_tables = [
        "Leveling",
        "Economy",
        "Birthdays",
        "Family",
        "CustomVCPresets"
    ]

    async with _ActivePool.acquire() as conn:
        async with conn.cursor() as cursor:
            try:
                for table in dependent_tables:
                    try:
                        await cursor.execute(
                            f"INSERT IGNORE INTO `ElectroAI`.`{table}` (`UserID`) SELECT `UserID` FROM `ElectroAI`.`Users`;"
                        )
                    except Exception as e:
                        print(f"Error backfilling users in table {table}: {e}")
                await conn.commit()
            except Exception as e:
                await conn.rollback()
                print(f"Error backfilling users: {e}")