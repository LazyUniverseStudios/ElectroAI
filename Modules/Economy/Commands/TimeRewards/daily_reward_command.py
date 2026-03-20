import discord
from discord import embeds
from discord.ext import commands
from InternalLogic.DatabaseLogic.DBQueries.DBQueries_Economy import ClaimDailyReward
from datetime import datetime, timedelta, timezone
from config import EmbedColor, EmbedColor_Error

@commands.command(name='daily', aliases=["dailyreward"])
async def daily_reward_command(ctx):
    user_id = ctx.author.id

    result, next_use_time = await ClaimDailyReward(user_id)

    if result is None:
        embed = discord.Embed(
            title="Database Error", 
            description="I couldn't reach the database. Please try again in a few moments, or contact support if the issue persists.", 
            color=EmbedColor_Error
        )
    elif result is True:
        unix_timestamp = int(next_use_time.timestamp())
        embed = discord.Embed(
            title="Reward Claimed!", 
            description=f"You've received 1,000 coins!\nYour next reward is available <t:{unix_timestamp}:R>.", 
            color=EmbedColor
        )
        embed.set_footer(text="Come back tomorrow!")
    else:
        if next_use_time:
            unix_timestamp = int(next_use_time.timestamp())
            cooldown_msg = f"You're too early! You can claim again <t:{unix_timestamp}:R>."
        else:
            cooldown_msg = "You've already claimed this recently."

        embed = discord.Embed(
            title="On Cooldown", 
            description=cooldown_msg, 
            color=EmbedColor_Error
        )

    await ctx.send(embed=embed)