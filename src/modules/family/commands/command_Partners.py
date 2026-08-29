import discord

from discord import Embed
from discord.ext import commands

from config import embedColor

from modules.family.db.check_Spouse import check_spouse

@commands.command(name="partners", aliases=["spouses", "spouse", "partner"])
async def partners(ctx, target: discord.Member = None):
    if target is None:
        target = ctx.author

    user_id = target.id

    spouses = await check_spouse(user_id)
    spouse_usernames = []

    if spouses [0] == None and spouses[1] == None and spouses[2] == None and spouses[3] == None and spouses[4] == None:
        embed = Embed(
            title="No Partners Found",
            description=f"{target.display_name} currently has no partners.",
            color=embedColor["DEFAULT"]
        )
        await ctx.send(embed=embed)
        return

    for spouse in spouses:
        if spouse is not None:
            spouse_profile = await ctx.guild.fetch_member(spouse)
            spouse_usernames.append(f"{spouse_profile.name} - {spouse_profile.mention}")

    embed_desc = f"{target.display_name} is married to:\n"
    for i in spouse_usernames:
        embed_desc += f"- {i}\n"


    embed = Embed(
        title=f"{target.display_name}'s Partners",
        description=embed_desc,
        color=embedColor["DEFAULT"]
    )

    await ctx.send(embed=embed)
