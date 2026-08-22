from discord.ext import commands
from discord import Embed

from config import roleIDs, channelIDs, embedColor

from modules.confessions.logic.modal_SubmitConfession import sendConfessionModalMessage

@commands.command(name="initconfess")
async def init_confessions(ctx):
    """
    Initializes the confessions feature by sending a sticky message in the designated confessions channel.
    This command is intended to be used by administrators to set up the confessions feature.

    Args:
        ctx (commands.Context): The context of the command invocation.
    """

    if roleIDs["STAFF_ROLES"]["LEAD_MANAGEMENT"] not in [role.id for role in ctx.author.roles]:
        embed = Embed(
            title="Permission Denied",
            description="You do not have the required permissions to use this command.",
            color=embedColor["ERROR"]
        )
        await ctx.send(embed=embed)
        return

    if ctx.channel.id != channelIDs["CONFESSIONS_CHANNEL"]:
        embed = Embed(
            title="Wrong Channel",
            description=f"This command can only be used in the <#{channelIDs['CONFESSIONS_CHANNEL']}> channel.",
            color=embedColor["ERROR"]
        )
        await ctx.send(embed=embed)
        return

    await sendConfessionModalMessage(ctx.bot)