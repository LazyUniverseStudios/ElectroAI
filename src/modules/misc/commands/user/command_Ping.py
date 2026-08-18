import discord
from config import embedColor
from discord.ext import commands

@commands.command(name="ping", aliases=["latency"])
async def ping(ctx):
    """
    Responds with the bot's latency in milliseconds.

    Args:
        ctx: The context of the command.
    """
    latency_ms = round(ctx.bot.latency * 1000)  # Convert latency to milliseconds
    embed = discord.Embed(
        title="Pong!",
        description=f"Latency: {latency_ms} ms",
        color=embedColor["DEFAULT"]
    )
    embed.set_footer(text=".ping")
    await ctx.send(embed=embed)