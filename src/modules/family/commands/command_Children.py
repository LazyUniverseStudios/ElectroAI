import discord

from discord import Embed
from discord.ext import commands

from config import embedColor

from modules.family.db.check_Children import check_children

@commands.command(name="children", aliases=["kids"])
async def children(ctx, target: discord.Member = None):
    if target is None:
        target = ctx.author

    user_id = target.id

    children = await check_children(user_id)
    children_usernames = []

    if children[0] is None and children[1] is None and children[2] is None and children[3] is None and children[4] is None and children[5] is None and children[6] is None:
        embed = Embed(
            title="No Children Found",
            description=f"{target.display_name} currently has no children.",
            color=embedColor["DEFAULT"]
        )
        await ctx.send(embed=embed)
        return

    for children in children:
        if children is not None:
            children_profile = await ctx.guild.fetch_member(children)
            children_usernames.append(f"{children_profile.name} - {children_profile.mention}")

    embed_desc = f"{target.display_name} is a parent to:\n"
    for i in children_usernames:
        embed_desc += f"- {i}\n"


    embed = Embed(
        title=f"{target.display_name}'s Children",
        description=embed_desc,
        color=embedColor["DEFAULT"]
    )

    await ctx.send(embed=embed)