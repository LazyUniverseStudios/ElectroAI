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

# Entry point
if __name__ == "__main__":
    main()