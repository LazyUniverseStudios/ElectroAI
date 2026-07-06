# Command In Progress - Do Not Use

import discord
from discord.ext import commands
from InternalLogic.DatabaseLogic.DBQueries.DBQueries_Economy import FetchUserBalance
from config import EmbedColor, EmbedColor_Error

@commands.command(name='balance', aliases=['bal'])
async def balance_command(ctx, target: discord.Member = None):
    if target is None:
        target = ctx.author

    user_id = target.id
    balance = await FetchUserBalance(user_id)

    if balance is None:
        embed = discord.Embed(
            title="No Balance Found", 
            description=f"{target.display_name} doesn't have a balance yet. They can earn coins by claiming rewards or participating in events!", 
            color=EmbedColor_Error
        )
    else:
        embed = discord.Embed(
            title=f"{target.display_name}'s Balance", 
            description=f"{target.display_name} has {balance} coins.", 
            color=EmbedColor
        )
    
    await ctx.send(embed=embed)
