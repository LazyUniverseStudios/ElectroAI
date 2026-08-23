import db_connection

async def set_child_adoption(parent_id, child_id, slot):
    async with db_connection._ActivePool.acquire() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(f"""
                UPDATE Family 
                SET Child{slot}ID = %s 
                WHERE UserID = %s""", 
                (child_id, parent_id)
            )
            await connection.commit()

async def set_child_removal(parent_id, child_id):
    async with db_connection._ActivePool.acquire() as connection:
        async with connection.cursor() as cursor:
            for i in range(1, 7):
                await cursor.execute("""
                    UPDATE Family
                    SET 
                        Child1ID = IF(Child1ID = %s, NULL, Child1ID),
                        Child2ID = IF(Child2ID = %s, NULL, Child2ID),
                        Child3ID = IF(Child3ID = %s, NULL, Child3ID),
                        Child4ID = IF(Child4ID = %s, NULL, Child4ID),
                        Child5ID = IF(Child5ID = %s, NULL, Child5ID),
                        Child6ID = IF(Child6ID = %s, NULL, Child6ID)
                    WHERE UserID = %s
                """, (
                    child_id,
                    child_id,
                    child_id,
                    child_id,
                    child_id,
                    child_id,
                    parent_id,
                ),
            )
            await connection.commit()