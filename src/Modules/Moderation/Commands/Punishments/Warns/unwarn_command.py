# Command In Progress - Do Not Use

import discord
from discord.ext import commands
from discord import embeds
from config import EmbedColor_Error, EmbedColor_Success
from InternalLogic.DatabaseLogic.DBQueries.DBQueries_Cases import DeleteCase


@commands.command(name="unwarn", aliases=["uw"])
async def unwarn_command(ctx, caseID = None):
    author = ctx.author
    bot = ctx.guild.me

    if bot.guild_permissions.manage_messages or bot.guild_permissions.administrator:
        pass
    else:
        embed = embeds.Embed(title="Error", description="I do not have permission to unwarn members.", color=EmbedColor_Error)
        await ctx.send(embed=embed)
        return
    
    if author.guild_permissions.manage_messages or author.guild_permissions.administrator:
        pass
    else:
        embed = embeds.Embed(title="Error", description="You do not have permission to unwarn members.", color=EmbedColor_Error)
        await ctx.send(embed=embed)
        return


    if caseID == None:
        embed = embeds.Embed(title="Error", description="Please specify a case ID.", color=EmbedColor_Error)
        await ctx.send(embed=embed)
        return
    
    await DeleteCase(caseID)
    embed = embeds.Embed(title="Success", description=f"Case {caseID} has been deleted and the warning has been removed.", color=EmbedColor_Success)
    await ctx.send(embed=embed)
    