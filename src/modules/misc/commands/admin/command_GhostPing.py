import discord

from discord.ext import commands
from discord import Embed

from config import roleIDs, embedColor

@commands.command(name="ghostping", aliases=["gp", "ghost", ])
async def ghost_ping(ctx):
    """
    Sends a ghost ping to the user who invoked the command.

    Args:
        ctx: The context of the command.
    """
    # Check if the command invoker has the required role to use the command
    if roleIDs["STAFF_ROLES"]["LEAD_MANAGEMENT"] not in [role.id for role in ctx.author.roles]:
        embed = Embed(
                    title="Error: Insufficient Permissions",
                    description="You do not have permission to use this command.",
                    color=embedColor["ERROR"]
                )
        embed.set_footer(text=".ghostping")
        await ctx.send(embed=embed)

    # Execute the command
    ping = f"<@&{roleIDs['BASE_MEMBER_ROLE']}>"
    await ctx.message.delete()  # Delete the command message to create a ghost ping effect
    pingmsg = await ctx.send(ping)  # Send the ping message
    await pingmsg.delete(delay=0.5)  # Delete the ping message after 0.5 seconds
    
        
