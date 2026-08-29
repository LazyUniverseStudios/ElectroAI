import db_connection

from config import channelIDs

from modules.confessions.logic.modal_SubmitConfession import sendConfessionModalMessage

async def getConfessionPersistence(bot):
    async with db_connection._ActivePool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT MessageID FROM Persistent_Messages WHERE MessagePurpose = %s", ("Confession_Sticky",))
            result = await cursor.fetchone()

    if result:
        message_id = result[0]
        channel = channelIDs["CONFESSION_CHANNEL"]
        message = await channel.fetch_message(message_id)  # Fetch the message using the bot instance
        if message:
            return [True, message]
        else:
            await sendConfessionModalMessage(bot)  # Send a new message if the old one is not found
            return [False, None]
    else:
        await sendConfessionModalMessage(bot)  # Send a new message if no record is found
        return [False, None]