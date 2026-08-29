import discord

from discord import Embed
from discord.ext import commands

from config import embedColor

from modules.family.db.check_Parent import check_parent

@commands.command(name="parents", aliases=["parent"])
async def parents(ctx, target: discord.Member = None):
    if target is None:
        target = ctx.author

    user_id = target.id

    parents = await check_parent(user_id)
    parent_usernames = []

    if parents[1] is None:
        embed = Embed(
            title="No Parent Found",
            description=f"{target.display_name} currently has no parent.",
            color=embedColor["DEFAULT"]
        )
        await ctx.send(embed=embed)
        return

    parentDcObj = await ctx.guild.fetch_member(parents[1])

    embed_desc = f"{target.display_name} is a child of:\n- {parentDcObj.name} - {parentDcObj.mention}\n"

    embed = Embed(
        title=f"{target.display_name}'s Parents",
        description=embed_desc,
        color=embedColor["DEFAULT"]
    )

    await ctx.send(embed=embed)