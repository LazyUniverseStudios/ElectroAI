from discord.ext import commands
import discord  
from config import EmbedColor_Misc
from InternalLogic.DatabaseLogic.DBQueries.DBQueries_Economy import UpdateServerEconomy_Reset

@commands.command(name='econresetserver')
async def econ_resetserver_command(ctx):
    author_id = ctx.author.id
    if author_id != 757868967384711249:
        await ctx.send("You do not have permission to use this command.")
        return
    await UpdateServerEconomy_Reset()
    embed = discord.Embed(title="Economy Reset", description="The economy data for all users has been reset.", color=EmbedColor_Misc)
    await ctx.send(embed=embed)