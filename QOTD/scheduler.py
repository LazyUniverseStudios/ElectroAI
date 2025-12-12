import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from questions import get_random_question
from discord import Embed

scheduler = AsyncIOScheduler()

async def send_daily_question(client):
    await client.wait_until_ready()
    channel = client.get_channel(1435649305586434089)
    pingrole = client.get_role(1412102087663157360)

    deck, question, question_key = get_random_question()
    embed = Embed(title="Question of the Day")
    embed.description = question
    embed.set_footer(text=f"{deck} | {question_key}")
    await channel.send(pingrole.mention, embed=embed)
    print(f"Sent question: {question}")

def start_qotdscheduler(client):
    @scheduler.scheduled_job('cron', hour=17, minute=0)
    async def scheduled_job():
        await send_daily_question(client)

    if not scheduler.running:
        scheduler.start()
