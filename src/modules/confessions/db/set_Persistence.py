import db_connection

async def set_ConfessionPersistence(messageID: int):
    """
    Saves the Persistent MessageID to the Database

    Args:
        messageID:
            The ID of the message to be saved.
    """

    MessagePurpose = "Confession_Sticky"

    async with db_connection._ActivePool.acquire() as conn:
        async with conn.cursor() as cursor:
            try:
                await cursor.execute("""
                                    INSERT INTO Persistent_Messages (MessageID, MessagePurpose)
                                    VALUES (%s, %s)
                                    ON DUPLICATE KEY UPDATE MessageID = VALUES(MessageID)
                                    """, (messageID, MessagePurpose))
                await conn.commit()
            except Exception as e:
                print(f"Error setting confession persistence: {e}")
                await conn.rollback()