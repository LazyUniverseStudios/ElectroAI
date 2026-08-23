import db_connection

async def set_parent(parent_id, child_id):
    async with db_connection._ActivePool.acquire() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute("""
                UPDATE Family 
                SET ParentID = %s 
                WHERE UserID = %s""", 
                (parent_id, child_id)
            )
            await connection.commit()