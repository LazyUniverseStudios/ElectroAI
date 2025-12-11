from discord import Embed
import discord

async def on_message(message):

    ## Boosts
    if message.type == discord.MessageType.premium_guild_subscription:
        embed = Embed(title="Thank You!", description=f"Thank You For Boosting The Server, {message.author.mention}!", color=0xe91e63)
        embed.set_thumbnail(url=message.author.avatar)
        await message.channel.send(embed=embed, content=f"{message.author.mention}")
