from discord.ext import commands
import discord
from config import EmbedColor_Error
from config import EmbedColor_Success
from InternalLogic.DatabaseLogic.DBQueries.DBQueries_Birthdays import SetUserBirthday
from typing import Optional

@commands.command(name='birthdayset')
async def birthday_set_command(ctx, target: Optional[discord.Member] = None, *, date: str = None):
    if target is None:
        target = ctx.author
    
    if date is None:
        embed = discord.Embed(title="Birthday Set Command", description="Please provide a date for the birthday. Format: DD-MM", color=EmbedColor_Error)
        await ctx.send(embed=embed)
        return
    
    # Validate the date format
    try:
        day, month = map(int, date.split('-'))
        if not (1 <= day <= 31 and 1 <= month <= 12):
            raise ValueError
    except ValueError:
        embed = discord.Embed(title="Birthday Set Command", description="Invalid date format. Please use DD-MM format.", color=EmbedColor_Error)
        await ctx.send(embed=embed)
        return
    date = date.zfill(5)
    # Assuming 'date' is verified as DD-MM (e.g., "29-01")
    day, month = date.split('-')
    formatted_date = f"1970-{month.zfill(2)}-{day.zfill(2)}"
    
    # Store the birthday in the database
    await SetUserBirthday(target.id, formatted_date)
    embed = discord.Embed(title="Birthday Set Command", description=f"Successfully set birthday for {target.mention} to {date}.", color=EmbedColor_Success)