import os
import discord
from discord.ext import commands
import sys
from config import embedColor
import subprocess

@commands.command(name='restart')
async def restart_command(ctx):
    author_id = ctx.author.id
    if author_id != 757868967384711249:
        await ctx.send("You do not have permission to use this command.")
        return
    embed = discord.Embed(title="Restarting...", description="The bot is restarting. Please wait a moment.", color=embedColor["MISC"])
    await ctx.send(embed=embed)
    await ctx.bot.close()
    subprocess.Popen([sys.executable] + sys.argv)
    os._exit(0)