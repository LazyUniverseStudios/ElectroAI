import discord

from discord import Embed
from discord.ext import commands

from config import embedColor, roleIDs

@commands.command(name="chatrevive", aliases=["cr", "reviveping"])
async def chatrevive(ctx):
    if roleIDs["STAFF_ROLES"]["HEAD_ADMIN"] not in [role.id for role in ctx.author.roles]:
        embed = Embed(
                    title="Error: Insufficient Permissions",
                    description="You do not have permission to use this command.",
                    color=embedColor["ERROR"]
                )
        embed.set_footer(text=".chatrevive")
        await ctx.send(embed=embed)
        return

    # Execute the command
    ping = f"<@&{roleIDs['CHAT_REVIVE_PING_ROLE']}>"
    await ctx.message.delete()  # Delete the command message to create a ghost ping effect
    await ctx.send(ping)  # Send the ping message