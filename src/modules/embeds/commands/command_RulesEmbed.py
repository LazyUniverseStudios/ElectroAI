import discord

from discord import Embed
from discord.ext import commands

from config import roleIDs, embedColor

@commands.command(name="embed_rules")
async def rules_embed(ctx):
    """
    Sends an embed message containing the server rules.

    Args:
        ctx: The context of the command.
    """
    if roleIDs["STAFF_ROLES"]["LEAD_MANAGEMENT"] not in [role.id for role in ctx.author.roles]:
        embed = Embed(
            title="Error: Insufficient Permissions",
            description="You do not have permission to use this command.",
            color=embedColor["ERROR"]
        )
        embed.set_footer(text=".embed rules")
        await ctx.send(embed=embed)
        return

    await ctx.message.delete()  # Delete the command message to keep the channel clean

    embed = Embed(
        title="<:electro_exclammark:1414667367182631103><:electro_heartdot:1414667665485598852>Electro Cafe™ Discord Rules<:electro_heartdot:1414667665485598852><:electro_exclammark:1414667367182631103>",
        description="",
        color=embedColor["DEFAULT"]
    )
    embed.add_field(
        name="<:electro_exclammark:1414667367182631103> Rule #1 | Follow Discord's Terms of Service",
        value="All members of this server must adhere to Discord's Terms of Service and Community Guidelines, any violations of these will result in immediate termination of your membership here.\n\n**Discord's Terms of Service** can be found [here](https://discord.com/terms)\n**Discord's Community Guidelines** can be found [here](https://discord.com/guidelines).\n‎",
        inline=False
    )
    embed.add_field(
        name="<:electro_exclammark:1414667367182631103> Rule #2 | Keep it Civil and Respectful",
        value="Members are expected to treat each other with respect at all times. **Slurs**, **Hate Speech**, **Derogatory Remarks** and **Discriminatory Language** are not welcome here. This is a safe space for everyone, and we will not tolerate any form of harassment or bullying. This includes threats, be it joke or not. No threats of violence, abuse or terror.\n‎",
        inline=False
    )
    embed.add_field(
        name="<:electro_exclammark:1414667367182631103> Rule #3 | Keep Content Appropriate",
        value="All content/media shared in this server must be appropriate for all audiences. Don't send here what you wouldn't send to your boss, keep it Safe for Work. This includes, but is not limited to: Pornography, Explicit/Suggestive Sexual Content, Gore, and Graphic Violence. This is a family-friendly server, and we expect all members to adhere to this standard.\n‎",
        inline=False
    )
    embed.add_field(
        name="<:electro_exclammark:1414667367182631103> Rule #4 | No Divisive Topics or Drama",
        value="Keep chat relaxed and friendly by avoiding divisive subjects, including **politics, religion, and war**. If a heated argument begins, do not engage - tag a moderator. Always respect staff requests to drop a conversation or take it to DMs.\n‎",
        inline=False,
    )
    embed.add_field(
        name="<:electro_exclammark:1414667367182631103> Rule #5 | Chat Etiquette & Language",
        value="Use English **only** in public channels for ease of moderation and clear communication. No spamming (text walls, repeated messages, excessive pings & emojis, repeatedly posting the same image). Keep topics relevant to their designated channels. Attempting to bypass bot filters, blacklisted words, or slowmode is strictly prohibited.\n‎",
        inline=False,
    )
    embed.add_field(
        name="<:electro_exclammark:1414667367182631103> Rule #6 | Advertising & Self-Promotion",
        value="Unsolicited self-promotion and advertising (including other Discord servers, streams, or commercial links) are not permitted without prior approval from staff.\nSharing Content: You are welcome to share relevant, high quality creative work (such as art, original videos, or projects) in our Media channels. \nPermission: If you wish to partner or promote an external project, please create a ticket first.\n‎",
        inline=False,
    )
    embed.add_field(
        name="<:electro_exclammark:1414667367182631103> Rule #7 | Respect Staff",
        value="The staff team reserve the right to take moderation action if they deem necessary. The staff are here to protect the server and keep the community safe. Follow staff's instructions. Higherups have the final say. Any attempt to impersonate or mimic a member of staff's identity, be it visually or behaviourally will be punished. Do not waste staff's time with false reports.\n‎",
        inline=False,
    )
    embed.add_field(
        name="<:electro_exclammark:1414667367182631103> Rule #8 | Use Common Sense",
        value="If something isn't stated here in the rules, but it is against common sense/ethics/morals, don't do it. We can and will still punish you for it. Moderators have the right to give out punishments at their discretion. If someone asks you to stop saying something to them or stop talking to them all together, stop. Otherwise, this is called harassment, of which is not tolerated at all in this server.\n‎",
        inline=False,
    )

    embed.set_footer(text="Electro Cafe™ | Rules | These rules may be updated at any time, with or without notice. By chatting here you therefore agree to abide by these rules. These rules were last updated 12th August 2026")
    
    await ctx.send(embed=embed)
