import discord
import os
import dotenv
import random
import requests

from discord.ext import commands

from config import COMMAND_PREFIX

import Modules

dotenv.load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents, help_command=None, case_insensitive=True)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')

bot.add_listener(Modules.Listeners.joins.on_member_join)
bot.add_listener(Modules.Listeners.leaves.on_member_remove)

if __name__ == "__main__":
    bot.run(BOT_TOKEN)