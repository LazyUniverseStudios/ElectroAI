import discord
from discord import embeds
from discord.ext import commands
from InternalLogic.DatabaseLogic.DBQueries.DBQueries_Economy import ClaimWeeklyReward
from datetime import datetime, timedelta, timezone

@commands.command(name='weekly', aliases=["weeklyreward"])
async def weekly_reward_command(ctx):
    author = ctx.author

    if author.premium_since is None:
        embed = discord.Embed(
            title="Boost Required", 
            description="This reward is exclusive to Nitro Boosters! Consider boosting the server to gain access to this and other perks.", 
            color=0xFF0000
        )
        await ctx.send(embed=embed)
        return
    
    user_id = author.id

    result, next_use_time = await ClaimWeeklyReward(user_id)

    if result is None:
        embed = discord.Embed(
            title="Database Error", 
            description="I couldn't reach the database. Please try again in a few moments, or contact support if the issue persists.", 
            color=0xFF0000
        )
    elif result is True:
        unix_timestamp = int(next_use_time.timestamp())
        embed = discord.Embed(
            title="Reward Claimed!", 
            description=f"You've received 2,000 coins!\nYour next reward is available <t:{unix_timestamp}:R>.", 
            color=0x00FF00
        )
        embed.set_footer(text="Come back next week!")
    else:
        if next_use_time:
            unix_timestamp = int(next_use_time.timestamp())
            cooldown_msg = f"You're too early! You can claim again <t:{unix_timestamp}:R>."
        else:
            cooldown_msg = "You've already claimed this recently."

        embed = discord.Embed(
            title="On Cooldown", 
            description=cooldown_msg, 
            color=0xFFEE00
        )
    
    await ctx.send(embed=embed)