import discord
from discord.ext import commands
import random
from InternalLogic.DatabaseLogic.DBQueries.DBQueries_Economy import FetchUserBalance, UpdateUserBalance_Add, UpdateUserBalance_Subtract
from config import EmbedColor, EmbedColor_Error

@commands.command(name='coinflip', aliases=['cf'])
async def coinflip_command(ctx, bet_amount: int = None, user_guess: str = None):
    user_id = ctx.author.id
    outcomes = ['heads', 'tails']
    balance = await FetchUserBalance(user_id)
    if user_guess is None:
        user_guess = 'heads'
    
    if bet_amount is None:
        embed = discord.Embed(
            title="Coin Flip Game", 
            description="To play, use the command with your bet amount and guess:\n`!coinflip <bet_amount> <heads/tails>`\nExample: `!coinflip 100 heads`", 
            color=EmbedColor
        )
        await ctx.send(embed=embed)
        return
    
    if bet_amount <= 0:
        embed = discord.Embed(
            title="Invalid Bet", 
            description="Your bet amount must be a positive integer.", 
            color=EmbedColor_Error
        )
        await ctx.send(embed=embed)
        return
    
    if balance is None or balance < bet_amount:
        embed = discord.Embed(
            title="Insufficient Funds", 
            description=f"You don't have enough coins to place that bet. Your current balance is {balance if balance is not None else 0} coins.", 
            color=EmbedColor_Error
        )
        await ctx.send(embed=embed)
        return

    await UpdateUserBalance_Subtract(user_id, bet_amount)

    if user_guess.lower() == "h":
        user_guess = "heads"
    elif user_guess.lower() == "t":
        user_guess = "tails"

    if user_guess not in outcomes:
        user_guess = "heads"

    flip_result = random.choice(outcomes)

    if user_guess == flip_result:
        bet_amount *= 2
        await UpdateUserBalance_Add(user_id, bet_amount)
        balance = await FetchUserBalance(user_id)
        embed = discord.Embed(
            title="You Win!", 
            description=f"The coin landed on {flip_result}! You won {bet_amount} coins! Your new balance is {balance} coins.", 
            color=EmbedColor
        )
    else:
        embed = discord.Embed(
            title="You Lose!", 
            description=f"The coin landed on {flip_result}. You lost {bet_amount} coins. Your new balance is {balance} coins.", 
            color=EmbedColor_Error
        )
    await ctx.send(embed=embed)