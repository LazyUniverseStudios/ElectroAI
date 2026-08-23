import discord

from modules.qotd.questions import getRandomQuestion

from config import embedColor

async def qotd(bot):
    guild = bot.get_guild(1216146656878133429)
    channel = guild.get_channel(1523838557624471625)
    pingRole = guild.get_role(1412102087663157360)

    deck, question, question_key = getRandomQuestion()

    embed = discord.Embed(
        title=f"Question of the Day - {deck}",
        description=question,
        color=embedColor["DEFAULT"]
    )
    embed.set_footer(text=f"Question ID: {question_key}")

    await channel.send(embed=embed)