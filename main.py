import discord
from discord.ext import commands

from config import *

intents = discord.Intents.all()
bot = commands.Bot(
    command_prefix=CMD_PREFIX,
    intents=intents,
    help_command=None,
    case_insensitive=CASE_INSENSITIVE
)

from Listeners import boosts
from Listeners import joins
from Listeners import leaves

@bot.add_listener(boosts.on_message)
@bot.add_listener(joins.on_member_join)
@bot.add_listener(leaves.on_member_remove)

def main():
    try:
        from config import BOT_TOKEN
        bot.run(BOT_TOKEN)
    except Exception as e:
        print(f"Error occurred while attempting to start the bot: {e}")

# Command Processing
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)

@bot.event
async def on_ready():
    print(f"Bot is ready! Logged in as {bot.user}")
    from QOTD import scheduler
    scheduler.start_qotdscheduler(bot)

# Entry point
if __name__ == "__main__":
    main()
