import discord

from datetime import datetime

from config import embedColor
from modules.birthdays.db.fetch_todays_birthdays import fetchTodaysBirthdays


async def birthdayCheck(bot):
    """
    Checks for users whose birthdays are today and sends a birthday message in the designated channels.

    Args:
        bot: The Discord bot instance.
    """
    guild = bot.get_guild(1216146656878133429) # Electro Cafe Guild
    channelA = guild.get_channel(1523831931710738544) # Birthday Channel
    channelB = guild.get_channel(1480599558642728990) # Main Lounge Chat Channel
    pingRole = guild.get_role(1412101967144026142) # Birthday Ping Role

    today = datetime.now().strftime("%m-%d")
    formattedToday = f"1970-{today}"

    try:
        birthdaysToday = await fetchTodaysBirthdays(formattedToday)
    except Exception as e:
        print(f"Error occurred while fetching today's birthdays: {e}")
        birthdaysToday = []

    if birthdaysToday:
        for userID in birthdaysToday:
            user = guild.get_member(userID)
            if user:
                embed = discord.Embed(
                    title="Happy Birthday! 🎉",
                    description=f"Today is {user.mention}'s birthday! Let's all wish them a fantastic day! 🎂",
                    color=embedColor.BIRTHDAY.value
                )
                if user.guild_avatar:
                    embed.set_thumbnail(url=user.guild_avatar.url)
                else:
                    embed.set_thumbnail(url=user.avatar.url)
                await channelA.send(embed=embed, content=f"{pingRole.mention}")
                await channelB.send(embed=embed)


