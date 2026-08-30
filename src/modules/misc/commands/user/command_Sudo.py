import discord

from discord import Embed, Permissions
from discord.ext import commands
from typing import Optional

from config import embedColor, command_Enabled

@commands.command(name="sudo", aliases=["mock"])
async def sudo(ctx, target: Optional[discord.Member] = None, *, message: str = None):
    perms = ctx.bot_permissions
    has_perms = perms.administrator or (perms.manage_messages and perms.manage_webhooks)

    if command_Enabled["Misc Commands"]["User"]["Sudo"] is False or command_Enabled["Misc Module"] is False:
        embed = Embed(
            title="Command Disabled",
            description="This command is currently disabled.",
            color=embedColor["ERROR"]
        )
        await ctx.send(embed=embed)
        return

    if not has_perms:
        embed = Embed(
            title="Insufficient Permissions",
            description="I need the following permissions to use this command:\n- Manage Messages\n- Manage Webhooks",
            color=embedColor["ERROR"]
        )
        await ctx.send(embed=embed)
        return

    if message is None:
        embed = Embed(
            title="Missing Message",
            description="Please provide a message to send.",
            color=embedColor["ERROR"]
        )
        await ctx.send(embed=embed)
        return

    if target is None:
        target = ctx.author

    await ctx.message.delete()

    channel = ctx.channel
    webhooks = await channel.webhooks()
    webhook = discord.utils.get(webhooks, name="SudoWebhook")

    if webhook is None:
        webhook = await channel.create_webhook(name="SudoWebhook")

    await webhook.send(message, username=target.display_name, avatar_url=target.display_avatar.url if target.avatar else None)