import db_connection

async def set_child(parent_id, child_id, slot):
    async with db_connection._ActivePool.acquire() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(f"""
                UPDATE Family 
                SET Child{slot}ID = %s 
                WHERE UserID = %s""", 
                (child_id, parent_id)
            )
            await connection.commit()