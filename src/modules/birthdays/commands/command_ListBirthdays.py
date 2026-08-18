import discord

from discord import Embed
from discord.ext import commands

from modules.birthdays.db.fetch_AllBirthdays import fetchAllBirthdays
from modules.birthdays.logic.formatter_OrdinalBirthdays import format_ordinal_date

from config import embedColor

@commands.command(name="listbirthdays", aliases=["listbdays", "listbday", "birthdaylist", "bdaylist"])
async def list_birthdays(ctx):
    """
    Lists all birthdays stored in the database.

    Args:
        ctx: The context of the command.
    """
    birthdays = await fetchAllBirthdays()

    if not birthdays:
            embed = Embed(
                title="Error: No Birthdays Found",
                description="No birthdays found in the database or an error connecting to the database.",
                color=embedColor.ERROR.value
            )
            await ctx.send(embed=embed)
            return

    birthdays.sort(key=lambda x: x[1])

    description_lines = []

    for user_id, birthday in birthdays:
        member = ctx.guild.get_member(user_id)
        if not member:
            try:
                member = await ctx.guild.fetch_member(user_id)
            except discord.NotFound:
                member = None
        user_mention = member.mention if member else f"Unknown User (`{user_id}`)"
        formatted_date = format_ordinal_date(birthday)
        
        description_lines.append(f"• **{formatted_date}** — {user_mention}")

    full_description = "\n".join(description_lines)


    embed = Embed(
         title="Birthday List", 
         description=full_description, 
         color=embedColor.DEFAULT.value
         )

    await ctx.send(embed=embed)