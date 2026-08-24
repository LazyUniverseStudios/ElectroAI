import discord
import os
import dotenv

from discord.ext import commands
from discord.ui import View, Button, button
from discord import ButtonStyle
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from db_manage_users import CreateUserIfNotExists, BackfillUsers
from modules.birthdays.logic.scheduler_BirthdayChecker import birthdayCheck
from modules.birthdays.logic.scheduler_BirthdayChecker import birthdayRoleRemove
from modules.qotd.logic.scheduler_QOTD import qotd

from db_connection import createPool

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

    try:
        await createPool()  # Create the database connection pool
        print("Database connection pool created successfully.")
    except Exception as e:
            pass


    dotenv.load_dotenv()
    # Schedules the birthday checker to run daily at midnight (00:00:00).
    try:
        scheduler.add_job(birthdayCheck, 'cron', hour=0, minute=0, second=0, args=[bot])
        print("Birthday checker started successfully.")
    except Exception as e:
        print(f"Error occurred while scheduling birthday checker: {e}")

    try:
        scheduler.add_job(birthdayRoleRemove, 'cron', hour=0, minute=0, second=0, args=[bot])
        print("Birthday role removal checker started successfully.")
    except Exception as e:
        print(f"Error occurred while scheduling birthday role remover: {e}")

    # Schedules the Question of the Day to run daily at 17:00:00.
    try:
        scheduler.add_job(qotd, 'cron', hour=17, minute=0, second=0, args=[bot])
        print("QOTD scheduler started successfully.")
    except Exception as e:
        print(f"Error occurred while scheduling QOTD scheduler: {e}")

    # Starts the scheduler to run the scheduled jobs.
    try:
        scheduler.start()
    except Exception as e:
        print(f"Error occurred while starting the scheduler: {e}")

    # Backfills existing users across the database, ensuring that all users are inserted into new dependent tables.
    try:
        await BackfillUsers()
    except Exception as e:
        print(f"Error occurred while backfilling users: {e}")

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

    # Command Registration
    ## General Commands
    ### User Commands
    #### Help Command
    from modules.misc.commands.user.command_Help import help_command
    bot.add_command(help_command)
    #### Ping Command
    from modules.misc.commands.user.command_Ping import ping
    bot.add_command(ping)

    ### Admin Commands
    #### Restart Command
    from modules.misc.commands.admin.command_Restart import restart_command
    bot.add_command(restart_command)
    #### Ghost Ping Command
    from modules.misc.commands.admin.command_GhostPing import ghost_ping
    bot.add_command(ghost_ping)


    ## Birthday Commands
    ### User Commands
    #### Birthday Set Command
    from modules.birthdays.commands.command_SetBirthday import birthday_set
    bot.add_command(birthday_set)
    #### Birthdays List Command
    from modules.birthdays.commands.command_ListBirthdays import list_birthdays
    bot.add_command(list_birthdays)


    ## Embed Commands
    ### Registers the `embed rules` command from the file `command_RulesEmbed`, allowing users to view the server rules in an embedded format.
    from modules.embeds.commands.command_RulesEmbed import rules_embed
    bot.add_command(rules_embed)


    ## Confessions Commands
    from modules.confessions.commands.comamnd_InitializeConfessions import init_confessions
    bot.add_command(init_confessions)


    ## Family Commands
    ### Adopt Command
    from modules.family.commands.command_Adopt import adopt
    bot.add_command(adopt)
    ### Marry Command
    from modules.family.commands.command_Marry import marry
    bot.add_command(marry)
    ### Runaway Command
    from modules.family.commands.command_Runaway import runaway
    bot.add_command(runaway)

    # View Registration
    persistentView = View(timeout=None)

    ## Confession Modal View
    from modules.confessions.logic.modal_SubmitConfession import confessionButtonCallback
    confess_button = Button(
        style=ButtonStyle.primary,
        label="Submit a Confession",
        emoji="🤫",
        custom_id="submit_confession_btn"  # Must match the custom_id used when sending
    )
    confess_button.callback = confessionButtonCallback
    persistentView.add_item(confess_button)

    bot.add_view(persistentView)

    # Confession Modal Creation
    try:
        from modules.confessions.db.get_Persistence import getConfessionPersistence
        await getConfessionPersistence(bot)
    except Exception as e:
        print(f"Error occurred while fetching confession persistence: {e}")

# Runs when the bot is ready and connected to Discord
@bot.event
async def on_ready():
    # Outputs the bot's username and ID to the console
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('------')

    # Iterates through all members, and inserting them into the database's Users table if they don't already exist.
    # This ensures that all members are accounted for in the database, even if they joined while the bot was offline.
    # Insertion activates a trigger, syncing new user IDs across dependent tables
    try:
        for guild in bot.guilds:
            for member in guild.members:
                if not member.bot:
                    await CreateUserIfNotExists(member.id)
    except Exception as e:
        print(f"Error occurred while creating users: {e}")

# Listens for messages in the server.
@bot.event
async def on_message(message):
    # Ignores messages sent by bots to prevent feedback loops or unnecessary processing
    if message.author.bot:
        return

    # Processes commands if the message is a command
    await bot.process_commands(message)

bot.run(BOT_TOKEN)