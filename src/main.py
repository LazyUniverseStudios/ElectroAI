import discord
import os
import dotenv
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from db_manage_users import CreateUserIfNotExists, BackfillUsers
from modules.birthdays.logic.scheduler_BirthdayChecker import birthdayCheck
from modules.qotd.logic.scheduler_QOTD import qotd

from discord.ext import commands

dotenv.load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(
    command_prefix=".", 
    intents=intents, 
    help_command=None, 
    case_insensitive=True)

scheduler = AsyncIOScheduler()

# Runs during the startup of the bot, ensuring it only runs once per session.
@bot.event
async def setup_hook():
    # Schedules the birthday checker to run daily at midnight (00:00:00) and starts the scheduler.
    try:
        scheduler.add_job(birthdayCheck, 'cron', hour=0, minute=0, second=0, args=[bot])
        scheduler.start()
        print("Birthday checker started successfully.")
    except Exception as e:
        print(f"Error occurred while scheduling birthday checker: {e}")

    # Schedules the Question of the Day to run daily at 17:00:00 and starts the scheduler.
    try:
        scheduler.add_job(qotd, 'cron', hour=17, minute=0, second=0, args=[bot])
        scheduler.start()
        print("QOTD scheduler started successfully.")
    except Exception as e:
        print(f"Error occurred while scheduling QOTD scheduler: {e}")

    # Backfills existing users across the database, ensuring that all users are inserted into new dependent tables.
    await BackfillUsers()

    # Listener Registration
    ## Boost Listener
    ### Registers the 'on_boost' function as a listener for the 'on_message' event.
    from modules.listeners.listeners.boosts import on_boost
    bot.add_listener(on_boost, 'on_message')
    ## Join Listener
    from modules.listeners.listeners.joins import on_member_join
    bot.add_listener(on_member_join, 'on_member_join')
    ## Leave Listener
    from modules.listeners.listeners.leaves import on_member_remove
    bot.add_listener(on_member_remove, 'on_member_remove')

# Runs when the bot is ready and connected to Discord
@bot.event
async def on_ready():
    # Outputs the bot's username and ID to the console
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('------')

    # Iterates through all members, and inserting them into the database's Users table if they don't already exist.
    # This ensures that all members are accounted for in the database, even if they joined while the bot was offline.
    # Insertion activates a trigger, syncing new user IDs across dependent tables
    for guild in bot.guilds:
        for member in guild.members:
            if not member.bot:
                await CreateUserIfNotExists(member.id)

# Listens for messages in the server.
@bot.event
async def on_message(message):
    # Ignores messages sent by bots to prevent feedback loops or unnecessary processing
    if message.author.bot:
        return

    # Processes commands if the message is a command
    await bot.process_commands(message)

bot.run(BOT_TOKEN)