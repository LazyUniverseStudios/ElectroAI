import db_connection

async def set_partner_marry(partnerA_id, partnerB_id, slot):
    async with db_connection._ActivePool.acquire() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(f"""
                UPDATE Family
                SET Partner{slot}ID = %s
                WHERE UserID = %s""", 
                (partnerB_id, partnerA_id)
            )
            await connection.commit()

async def set_partner_divorce(partnerA_id, partnerB_id):
    async with db_connection._ActivePool.acquire() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute("""
                UPDATE Family
                SET 
                    Partner1ID = IF(Partner1ID = %s, NULL, Partner1ID),
                    Partner2ID = IF(Partner2ID = %s, NULL, Partner2ID)
                WHERE UserID = %s""",
                (partnerA_id, partnerA_id, partnerB_id))
            await cursor.execute("""
                UPDATE Family
                SET 
                    Partner1ID = IF(Partner1ID = %s, NULL, Partner1ID),
                    Partner2ID = IF(Partner2ID = %s, NULL, Partner2ID)
                WHERE UserID = %s""",
                (partnerB_id, partnerB_id, partnerA_id))
            await connection.commit()