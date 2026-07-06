import discord
from discord.ext import commands
from discord import Embed
from config import EmbedColor, EmbedColor_Error, EmbedColor_Success

@commands.command(name='ping')
async def ping_command(ctx):
    latency = round(ctx.bot.latency * 1000)
    embed = Embed(
        title="Pong!",
        description=f"Latency: {latency}ms",
        color=EmbedColor
    )
    await ctx.send(embed=embed)