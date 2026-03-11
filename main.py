import discord
import os
import dotenv

from discord.ext import commands

from config import COMMAND_PREFIX
dotenv.load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

from InternalLogic.DatabaseLogic.DBQueries import CreateUserIfNotExists

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents, help_command=None, case_insensitive=True)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    from Modules.QOTD.scheduler import start_qotdscheduler
    start_qotdscheduler(bot)

    for guild in bot.guilds:
        for member in guild.members:
            if not member.bot:
                await CreateUserIfNotExists(member.id)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

import Modules.Listeners.joins
bot.add_listener(Modules.Listeners.joins.on_member_join)
import Modules.Listeners.leaves
bot.add_listener(Modules.Listeners.leaves.on_member_remove)
import Modules.Listeners.boosts
bot.add_listener(Modules.Listeners.boosts.on_message)


import Modules.Misc.AdminCommands.restart
bot.add_command(Modules.Misc.AdminCommands.restart.restart_command)


import Modules.Moderation.Commands.Punishments.ban_command
bot.add_command(Modules.Moderation.Commands.Punishments.ban_command.ban_command)
import Modules.Moderation.Commands.Punishments.kick_command
bot.add_command(Modules.Moderation.Commands.Punishments.kick_command.kick_command)
import Modules.Moderation.Commands.Punishments.timeout_command
bot.add_command(Modules.Moderation.Commands.Punishments.timeout_command.timeout_command)
import Modules.Moderation.Commands.Punishments.warn_command
import Modules.Moderation.Commands.Punishments.unban_command
bot.add_command(Modules.Moderation.Commands.Punishments.unban_command.unban_command)
import Modules.Moderation.Commands.Punishments.untimeout_command
bot.add_command(Modules.Moderation.Commands.Punishments.untimeout_command.untimeout_command)
import Modules.Moderation.Commands.Punishments.unwarn_command

import Modules.Moderation.Commands.Channels.purge_command
import Modules.Moderation.Commands.Channels.lock_command
import Modules.Moderation.Commands.Channels.unlock_command

import Modules.Moderation.Commands.Cases.cases_command
import Modules.Moderation.Commands.Cases.case_delete_command
import Modules.Moderation.Commands.Cases.case_info_command
import Modules.Moderation.Commands.Cases.case_edit_command


import Modules.Economy.Commands.TimeRewards.daily_reward_command
import Modules.Economy.Commands.TimeRewards.weekly_reward_command
import Modules.Economy.Commands.TimeRewards.monthly_reward_command

import Modules.Economy.Commands.Transaction.shop_command


if __name__ == "__main__":
    bot.run(BOT_TOKEN)