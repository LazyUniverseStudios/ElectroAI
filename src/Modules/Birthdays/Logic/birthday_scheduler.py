import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from InternalLogic.DatabaseLogic.DBQueries.DBQueries_Birthdays import FetchTodaysBirthdays
from config import EmbedColor
import discord

scheduler = AsyncIOScheduler()

async def birthday_check(client):
    guild = client.get_guild(1216146656878133429)
    channel = guild.get_channel(1523831931710738544)
    pingrole = guild.get_role(1412101967144026142)

    today = datetime.now().strftime("%m-%d")
    formatted_today = f"1970-{today}"

    birthdays_today = await FetchTodaysBirthdays(formatted_today)

    if birthdays_today:
        for user_id in birthdays_today:
            target = guild.get_member(user_id)
            embed = discord.Embed(title="Happy Birthday!", description=f"Happy Birthday {target.mention}! 🎉🎂", color=EmbedColor)
            await channel.send(pingrole.mention, embed=embed)
            print(f"Sent birthday message for {target.name} ({target.id})")

def start_birthdayscheduler(client):
    @scheduler.scheduled_job('cron', hour=0, minute=0)
    async def scheduled_job():
        await birthday_check(client)

    if not scheduler.running:
        scheduler.start()