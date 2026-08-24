import discord

from discord import Embed, ButtonStyle
from discord.ext import commands
from discord.ui import Button, View

from config import embedColor

from modules.family.db.check_Spouse import check_spouse
from modules.family.db.set_Partner import set_partner_marry as set_partner

@commands.command()
async def marry(ctx, member: discord.Member = None):
    if member is None:
        embed = Embed(
            title="Error",
            description="Please specify a member to marry.",
            color=embedColor["ERROR"]
        )
        await ctx.send(embed=embed)
        return

    if member == ctx.author:
        embed = Embed(
            title="Error",
            description="You cannot marry yourself.",
            color=embedColor["ERROR"]
        )
        await ctx.send(embed=embed)
        return

    author_id = ctx.author.id
    target_id = member.id

    author_spouses = await check_spouse(author_id)
    target_spouses = await check_spouse(target_id)

    if author_spouses:
        if target_id in author_spouses:
            embed = Embed(
                title="Error",
                description=f"You are already married to <@{target_id}>.",
                color=embedColor["ERROR"]
            )
            await ctx.send(embed=embed)
            return

    if target_spouses:
        if author_id in target_spouses:
            embed = Embed(
                title="Error",
                description=f"<@{target_id}> is already married to you.",
                color=embedColor["ERROR"]
            )
            await ctx.send(embed=embed)
            return

    # Count active spouses
    author_count = sum(1 for s in author_spouses if s is not None)
    target_count = sum(1 for s in target_spouses if s is not None)

    if author_count >= 2:
        embed = Embed(
            title="Error",
            description="You cannot marry more than 2 people.",
            color=embedColor["ERROR"],
        )
        await ctx.send(embed=embed)
        return

    if target_count >= 2:
        embed = Embed(
            title="Error",
            description=f"<@{target_id}> already has 2 partners!",
            color=embedColor["ERROR"],
        )
        await ctx.send(embed=embed)
        return

    # Find the first available empty slot (1 or 2)
    author_slot = author_spouses.index(None) + 1
    target_slot = target_spouses.index(None) + 1

    marryConfirmationEmbed = Embed(
        title="Marriage",
        description=f"Are you sure you want to marry <@{target_id}>?",
        color=embedColor["DEFAULT"]
    )
    marryConfirmationView = View()

    marryConfirmationAcceptButton = Button(
        label="Yes",
        style=ButtonStyle.green
    )
    marryconfirmationDeclineButton = Button(
        label="No",
        style=ButtonStyle.red
    )

    async def marryConfirmationAcceptCallback(interaction):
        if interaction.user.id != author_id:
            await interaction.response.send_message("You are not authorized to confirm this marriage.", ephemeral=True)
            return

        marryConfirmationPt2Embed = Embed(
            title="Marriage",
            description=f"<@{target_id}>, <@{author_id}> wants to marry you! Do you accept?",
            color=embedColor["DEFAULT"]
        )

        marryConfirmationPt2View = View()

        marryConfirmationPt2AcceptButton = Button(
            label="Yes",
            style=ButtonStyle.green
        )

        marryConfirmationPt2DeclineButton = Button(
            label="No",
            style=ButtonStyle.red
        )

        async def marryConfirmationPt2AcceptCallback(interaction):
            if interaction.user.id != target_id:
                await interaction.response.send_message("You are not authorized to accept this marriage.", ephemeral=True)
                return

            try:
                await set_partner(author_id, target_id, author_slot)
                await set_partner(target_id, author_id, target_slot)
                embed = Embed(
                    title="Marriage Successful",
                    description=f"<@{author_id}> and <@{target_id}> are now married!",
                    color=embedColor["SUCCESS"]
                )
                await interaction.response.edit_message(embed=embed, view=None)
            except Exception as e:
                embed = Embed(
                    title="Error",
                    description="An error occurred while processing the marriage. Please try again later.",
                    color=embedColor["ERROR"]
                )
                await interaction.response.edit_message(embed=embed, view=None)
                return

        async def marryConfirmationPt2DeclineCallback(interaction):
            if interaction.user.id != target_id:
                await interaction.response.send_message("You are not authorized to decline this marriage.", ephemeral=True)
                return

            embed = Embed(
                title="Marriage Declined",
                description=f"Sorry <@{author_id}>, <@{target_id}> has declined your marriage proposal.",
                color=embedColor["ERROR"]
            )
            await interaction.response.edit_message(embed=embed, view=None)

        marryConfirmationPt2AcceptButton.callback = marryConfirmationPt2AcceptCallback
        marryConfirmationPt2DeclineButton.callback = marryConfirmationPt2DeclineCallback

        marryConfirmationPt2View.add_item(marryConfirmationPt2AcceptButton)
        marryConfirmationPt2View.add_item(marryConfirmationPt2DeclineButton)

        await interaction.response.edit_message(embed=marryConfirmationPt2Embed, view=marryConfirmationPt2View)

    async def marryConfirmationDeclineCallback(interaction):
        if interaction.user.id != author_id:
            await interaction.response.send_message("You are not authorized to decline this marriage.", ephemeral=True)
            return

        embed = Embed(
            title="Marriage Cancelled",
            description="You have cancelled your marriage proposal.",
            color=embedColor["ERROR"]
        )
        await interaction.response.edit_message(embed=embed, view=None)

    marryConfirmationAcceptButton.callback = marryConfirmationAcceptCallback
    marryconfirmationDeclineButton.callback = marryConfirmationDeclineCallback

    marryConfirmationView.add_item(marryConfirmationAcceptButton)
    marryConfirmationView.add_item(marryconfirmationDeclineButton)

    await ctx.send(embed=marryConfirmationEmbed, view=marryConfirmationView)