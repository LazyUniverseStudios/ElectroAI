import discord
import asyncio

async def create_ConfessionThread(message, threadName, autoArchiveDuration=60):
    """
    Creates a thread for a specific message in the Confessions channel.

    Args:
        messageID (int): The ID of the message to create a thread for.
        threadName (str): The name of the thread to be created.
        autoArchiveDuration (int, optional): The duration in minutes after which the thread will be automatically archived. Defaults to 60 minutes.

    Returns:
        discord.Thread: The created thread object.
    """

    try:
        thread = await message.create_thread(
            name=threadName,
            auto_archive_duration=60
        )

        confession_id = threadName[-3:] # Extract the confession ID from the thread name
    
        # Send starter message so Discord activates and displays the thread box
        await thread.send(
            f"Discussion thread for **Confession #{confession_id}**. Remember to keep the discussion respectful and adhere to server rules!"
        )
        return thread
    except discord.Forbidden:
        print("[Confessions] Missing 'Create Public Threads' or 'Send Messages in Threads' permissions.")
    except discord.HTTPException as e:
        print(f"[Confessions] Discord HTTP error creating thread: {e}")
    except Exception as e:
        print(f"[Confessions] Unexpected error creating thread: {e}")
    return None