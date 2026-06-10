from discord.ext import commands
import discord  
from config import EmbedColor_Misc
from InternalLogic.DatabaseLogic.DBQueries.DBQueries_Economy import UpdateUserEconomy_Reset

@commands.command(name='econresetuser')
async def econ_resetuser_command(ctx, user: discord.User = None):
    author_id = ctx.author.id
    if author_id != 757868967384711249:
        await ctx.send("You do not have permission to use this command.")
        return
    if user is None:
        await ctx.send("Please specify a user to reset their economy data.")
        return
    await UpdateUserEconomy_Reset(user.id)
    embed = discord.Embed(title="Economy Reset", description=f"The economy data for {user.mention} has been reset.", color=EmbedColor_Misc)
    await ctx.send(embed=embed)