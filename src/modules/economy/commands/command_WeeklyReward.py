import discord

from discord.ext import commands

from config import embedColor
from modules.economy.db.claim_WeeklyReward import claimWeeklyReward

@commands.command(name="weeklyreward", aliases=["weekly", "wr"])
async def weekly_reward(ctx):
    """
    Claims the weekly reward for the user. Requires the user to be a server booster.
    
    Args:
        ctx: The context of the command.
    """
    author = ctx.author

    if author.premium_since is None:
        embed = discord.Embed(
            title="Premium Required", 
            description="You need to be a booster to claim the weekly reward. Please consider boosting our server for use of this command and other perks.", 
            color=embedColor["ERROR"]
        )
        await ctx.send(embed=embed)
        return

    user_id = author.id
    success, next_use_time = await claimWeeklyReward(user_id)

    if success is None:
        embed = discord.Embed(
            title="Database Error", 
            description="I couldn't reach the database. Please try again in a few moments, or contact <@757868967384711249> if the issue persists.", 
            color=embedColor["ERROR"]
        )
    elif success is True:
        unix_timestamp = int(next_use_time.timestamp())
        embed = discord.Embed(
            title="Reward Claimed!", 
            description=f"You've received 3,000 coins!\nYour next reward is available <t:{unix_timestamp}:R>.", 
            color=embedColor["DEFAULT"]
        )
        embed.set_footer(text="Come back next week!")
    elif success is False:
        if isinstance(next_use_time, Exception):
            embed = discord.Embed(
                title="Database Error", 
                description="I couldn't reach the database. Please try again in a few moments, or contact <@757868967384711249> if the issue persists.", 
                color=embedColor["ERROR"]
            )
        elif next_use_time:
            unix_timestamp = int(next_use_time.timestamp())
            cooldown_msg = f"You're too early! You can claim again <t:{unix_timestamp}:R>."
        else:
            cooldown_msg = "You're too early! Please try again later."

        embed = discord.Embed(
            title="On Cooldown", 
            description=cooldown_msg, 
            color=embedColor["ERROR"]
        )
    await ctx.send(embed=embed)