import discord

from discord import Embed, ButtonStyle
from discord.ext import commands
from discord.ui import Button, View

from config import embedColor

from modules.family.db.check_Parent import check_parent
from modules.family.db.set_Child import set_child_removal
from modules.family.db.set_Parent import set_parent

@commands.command()
async def runaway(ctx):
    author_id = ctx.author.id

    parent = await check_parent(author_id)

    if parent[0] == False:
        embed = Embed(
            title="Error",
            description="You do not have a parent to runaway from.",
            color=embedColor["ERROR"]
        )
        await ctx.send(embed=embed)
        return

    runawayConfirmationEmbed = Embed(
        title="Runaway",
        description="Are you sure you want to runaway from your parent?",
        color=embedColor["DEFAULT"]
        )

    runawayConfirmationView = View()

    runawayConfirmationAcceptButton = Button(
        label="Yes",
        style=ButtonStyle.green
    )

    runawayConfirmationDeclineButton = Button(
        label="No",
        style=ButtonStyle.red
    )

    async def runawayConfirmationAcceptCallback(interaction):
        if interaction.user.id != author_id:
            await interaction.response.send_message("You are not authorized to confirm this runaway.", ephemeral=True)
            return

        try:
            await set_parent(None, author_id)
            await set_child_removal(parent[1], author_id)
            embed = Embed(
                title="Runaway Successful",
                description="You have successfully run away from your parent.",
                color=embedColor["SUCCESS"]
            )
            await interaction.response.send_message(embed=embed, view=None)
        except Exception as e:
            embed = Embed(
                title="Error",
                description="An error occurred while processing your running away. Please try again later.",
                color=embedColor["ERROR"]
            )
            await interaction.response.send_message(embed=embed, view=None)
            return

    async def runawayConfirmationDeclineCallback(interaction):
        if interaction.user.id != author_id:
            await interaction.response.send_message("You are not authorized to decline this runaway.", ephemeral=True)
            return

        embed = Embed(
            title="Runaway Cancelled",
            description="You have cancelled your runaway.",
            color=embedColor["ERROR"]
        )
        await interaction.response.send_message(embed=embed, view=None)

    runawayConfirmationAcceptButton.callback = runawayConfirmationAcceptCallback
    runawayConfirmationDeclineButton.callback = runawayConfirmationDeclineCallback

    runawayConfirmationView.add_item(runawayConfirmationAcceptButton)
    runawayConfirmationView.add_item(runawayConfirmationDeclineButton)

    await ctx.send(embed=runawayConfirmationEmbed, view=runawayConfirmationView)

        