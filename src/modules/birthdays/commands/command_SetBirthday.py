import discord

from discord import Embed
from discord.ext import commands
from typing import Optional

from modules.birthdays.db.set_UserBirthday import setUserBirthday

from config import embedColor

@commands.command(name="birthdayset", aliases=["bdayset", "setbday"])
async def birthday_set(ctx, target: Optional[discord.Member] = None, birthday: str = None):
    """
    Sets the birthday for a user. If no target is specified, it sets the birthday for the command invoker.

    Args:
        ctx: The context of the command.
        target (Optional[discord.Member]): The member whose birthday is being set. Defaults to the command invoker.
        birthday (str): The birthday in the format DD-MM.
    """
    # Checking if user has permission to set birthdays for others
    if ctx.author.id != 757868967384711249:
        if target is not None and target.id != ctx.author.id:
            embed = Embed(
                title="Error: Insufficient Permissions",
                description="You do not have permission to set birthdays for other users.",
                color=embedColor.ERROR.value
            )
            embed.set_footer(text=".birthdayset")
            await ctx.send(embed=embed)
            return

    # If no target is specified, default to the command invoker
    if target is None:
        target = ctx.author
    
    # Check Birthday Exists
    if birthday is None:
        embed = Embed(
            title="Error: No Birthday Provided",
            description="Please provide a birthday in the format DD-MM.",
            color=embedColor.ERROR.value
        )
        embed.set_footer(text=".birthdayset")
        await ctx.send(embed=embed)
        return
    
    # Validate Birthday Format
    try:
        day, month = map(int, birthday.split('-'))
        if month >= 1 and month <= 12:
            if day > 0:
                if month == 2 and day > 29:
                    raise ValueError
                elif month in [4, 6, 9, 11] and day > 30:
                    raise ValueError
                elif month in [1, 3, 5, 7, 8, 10, 12] and day > 31:
                    raise ValueError
            else:
                raise ValueError
        else:
            raise ValueError
    except ValueError:
        embed = Embed(
            title="Error: Invalid Birthday Format",
            description="Please provide a valid birthday in the format DD-MM.",
            color=embedColor.ERROR.value
        )
        embed.set_footer(text=".birthdayset")
        await ctx.send(embed=embed)
        return
    
    # Format Birthday for Database Storage
    formatted_birthday = f"1970-{month:02d}-{day:02d}"  # Store as YYYY-MM-DD for consistency

    # Set Birthday in Database
    success = await setUserBirthday(target.id, formatted_birthday)

    if success:
        embed = Embed(
            title="Birthday Set Successfully",
            description=f"{target.mention}'s birthday has been set to {day:02d}-{month:02d}.",
            color=embedColor.SUCCESS.value
        )
        embed.set_footer(text=".birthdayset")
        await ctx.send(embed=embed)
    else:
        embed=Embed(
            title="Error: Could Not Set Birthday",
            description="There was an error while trying to set the birthday. Please try again later, or contact <@757868967384711249> if the issue persists.",
            color=embedColor.ERROR.value)
        embed.set_footer(text=".birthdayset")
        await ctx.send(embed=embed)
