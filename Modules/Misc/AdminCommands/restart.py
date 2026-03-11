import discord
from discord.ext import commands
import os
import sys

from discord import embeds

@commands.command(name='restart', help='Restarts the bot (Admin only)')
async def restart_command(ctx):
    author_id = ctx.author.id
    if author_id != 757868967384711249:  # Replace with your Discord user ID
        await ctx.send("You do not have permission to use this command.")
        return
    embed = discord.Embed(title="Restarting...", description="The bot is restarting. Please wait a moment.", color=0x000000)
    await ctx.send(embed=embed)
    await ctx.bot.close()
    os.execv(sys.executable, ['python'] + sys.argv)
    
