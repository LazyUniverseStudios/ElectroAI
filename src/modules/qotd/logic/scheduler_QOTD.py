import discord

from modules.qotd.questions import getRandomQuestion

from config import embedColor, channelIDs, roleIDs

async def qotd(bot):
    guild = bot.get_guild(1216146656878133429)
    channel = guild.get_channel(channelIDs["QOTD_CHANNEL"])
    pingRole = guild.get_role(roleIDs["QOTD_PING_ROLE"])

    deck, question, question_key = getRandomQuestion()

    embed = discord.Embed(
        title=f"Question of the Day - {deck}",
        description=question,
        color=embedColor["DEFAULT"]
    )
    embed.set_footer(text=f"Question ID: {question_key}")

    message = await channel.send(embed=embed, content=pingRole.mention)
    await message.create_thread(name=f"QOTD - {question_key}", auto_archive_duration=1440, reason="QOTD Thread")
