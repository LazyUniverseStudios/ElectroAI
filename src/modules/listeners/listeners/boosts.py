from discord import Embed
import discord

from config import embedColor

async def on_boost(message):
    if message.type == discord.MessageType.premium_guild_subscription:
        embed = Embed(title="Thank You!", description=f"Thank You For Boosting The Server, {message.author.mention}!", color=embedColor.DEFAULT.value)
        embed.set_thumbnail(url=message.author.avatar)
        await message.channel.send(embed=embed, content=f"{message.author.mention}")