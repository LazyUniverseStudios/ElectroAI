from discord.ext import commands
import discord
from config import EmbedColor_Error

@commands.command(name='birthdayset')
async def birthday_set_command(ctx, target: discord.User = None, *, date: str = None):
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
    
    