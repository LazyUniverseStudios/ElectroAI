from discord import Embed
import discord
from InternalLogic.DatabaseLogic.DBQueries.DBQueries_Economy import UpdateUserBalance_Add
from config import EmbedColor

async def on_message(message):
    if message.type == discord.MessageType.premium_guild_subscription:
        embed = Embed(title="Thank You!", description=f"Thank You For Boosting The Server, {message.author.mention}!", color=EmbedColor)
        embed.set_thumbnail(url=message.author.avatar)
        await message.channel.send(embed=embed, content=f"{message.author.mention}")

        await UpdateUserBalance_Add(message.author.id, 1000)