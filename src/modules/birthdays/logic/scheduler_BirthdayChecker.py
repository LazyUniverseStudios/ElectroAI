import discord

from datetime import datetime, timedelta

from modules.birthdays.db.fetch_BirthdaysToday import fetchTodaysBirthdays

from config import embedColor
from config import serverIdentityIDs, channelIDs, roleIDs

global birthdayRoleUsers

async def birthdayCheck(bot):
    """
    Checks for users whose birthdays are today and sends a birthday message in the designated channels.

    Args:
        bot: The Discord bot instance.
    """
    guild = bot.get_guild(serverIdentityIDs["GUILD"]) # Electro Cafe Guild
    channelA = guild.get_channel(channelIDs["BIRTHDAY_CHANNEL"]) # Birthday Channel
    channelB = guild.get_channel(channelIDs["GENERAL_CHAT_CHANNEL"]) # Main Lounge Chat Channel
    pingRole = guild.get_role(roleIDs["BIRTHDAY_PING_ROLE"]) # Birthday Ping Role
    birthdayRole = guild.get_role(roleIDs["BIRTHDAY_ROLE"]) # Birthday Role

    birthdayRoleUsers = []

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
                    color=embedColor["BIRTHDAY"]
                )
                if user.guild_avatar:
                    embed.set_thumbnail(url=user.guild_avatar.url)
                else:
                    embed.set_thumbnail(url=user.avatar.url)
                await channelA.send(embed=embed, content=f"{pingRole.mention}")
                await channelB.send(embed=embed)
                await user.add_roles(birthdayRole, reason="Birthday Role Assignment")
                birthdayRoleUsers.append([user.id, datetime.now().strftime("%Y-%m-%d")])

async def birthdayRoleRemove(bot: discord.Client):
    """
    Removes the birthday role from anyone whose birthday is not today.
    Survives bot restarts without needing in-memory tracking.
    """
    guild = bot.get_guild(serverIdentityIDs["GUILD"])
    if not guild:
        return

    birthdayRole = guild.get_role(roleIDs["BIRTHDAY_ROLE"])
    if not birthdayRole:
        return

    today = datetime.now().strftime("%m-%d")
    formattedToday = f"1970-{today}"

    try:
        birthdaysToday = await fetchTodaysBirthdays(formattedToday)
    except Exception as e:
        print(f"Error fetching birthdays for role cleanup: {e}")
        birthdaysToday = []

    # Strip the role from anyone who currently has it but isn't on today's list
    for member in list(birthdayRole.members):
        if member.id not in birthdaysToday:
            await member.remove_roles(birthdayRole, reason="Birthday Role Expiration")