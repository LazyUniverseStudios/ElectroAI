# Command In Progress - Do Not Use

import discord
from discord.ext import commands
from discord import embeds
from config import EmbedColor_Error, EmbedColor_Success


@commands.command(name="unwarn", aliases=["uw"])
async def unwarn_command(ctx, target: discord.Member = None, caseID = None):
    author = ctx.author
    bot = ctx.guild.me

    if bot.guild_permissions.manage_messages or bot.guild_permissions.administrator:
        pass
    else:
        embed = embeds.Embed(title="Error", description="I do not have permission to manage messages.", color=EmbedColor_Error)
        await ctx.send(embed=embed)
        return
    
    if author.guild_permissions.manage_messages or author.guild_permissions.administrator:
        pass
    else:
        embed = embeds.Embed(title="Error", description="You do not have permission to manage messages.", color=EmbedColor_Error)
        await ctx.send(embed=embed)
        return
    
    
    if target == None:
        embed = embeds.Embed(title="Error", description="Please specify a user to unwarn.", color=EmbedColor_Error)
        await ctx.send(embed=embed)
        return

    if caseID == None:
        embed = embeds.Embed(title="Error", description="Please specify a case ID.", color=EmbedColor_Error)
        await ctx.send(embed=embed)
        return
    
    