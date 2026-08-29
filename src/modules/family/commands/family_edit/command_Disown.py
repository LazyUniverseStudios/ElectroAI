import discord

from discord import Embed, ButtonStyle
from discord.ext import commands
from discord.ui import Button, View, Select

from config import embedColor

from modules.family.db.check_Children import check_children
from modules.family.db.set_Child import set_child_removal
from modules.family.db.set_Parent import set_parent

@commands.command()
async def disown(ctx):
    author_id = ctx.author.id

    childslist = await check_children(author_id)

    emptySlots = sum(1 for s in childslist if s is None)

    if emptySlots >= 6:
        embed = Embed(
            title="Error",
            description="You are not married to anyone.",
            color=embedColor["ERROR"]
        )
        embed.set_footer(text=f".disown")
        await ctx.send(embed=embed)
        return

    disownSelectionEmbed = Embed(
        title="disown",
        description="Please select the child you want to disown from the dropdown menu below.",
        color=embedColor["DEFAULT"]
        )
    disownSelectionEmbed.set_footer(text=f".disown")

    disownSelectionView = View()

    disownSelectionDropdown = Select(
        placeholder="Select a child to disown",
        options=[
            discord.SelectOption(
                label = (await ctx.bot.fetch_user(child_id)).name, value=str(child_id)
                ) 
                for child_id in childslist if child_id is not None
                ]
    )

    disownSelectionDropdown.callback = disownSelectionCallback

    async def disownSelectionCallback(interaction):
        if interaction.user.id != author_id:
            await interaction.response.send_message("You are not authorized to select a child for disownment.", ephemeral=True)
            return

        global selected_child_id
        selected_child_id = int(disownSelectionDropdown.values[0])

        disownConfirmationEmbed = Embed(
            title="disown Confirmation",
            description=f"Are you sure you want to disown <@{selected_child_id}>?",
            color=embedColor["DEFAULT"]
        )

        disownConfirmationView = View()

        disownConfirmationAcceptButton = Button(
            label="Yes",
            style=ButtonStyle.green
        )

        disownConfirmationDeclineButton = Button(
            label="No",
            style=ButtonStyle.red
        )

        async def disownConfirmationAcceptCallback(interaction):
            if interaction.user.id != author_id:
                await interaction.response.send_message("You are not authorized to confirm this disownment.", ephemeral=True)
                return

            try:
                await set_child_removal(author_id, selected_child_id)
                await set_parent(None, selected_child_id)
                embed = Embed(
                    title="disown Successful",
                    description=f"You have successfully disowned <@{selected_child_id}>.",
                    color=embedColor["SUCCESS"]
                )
                await interaction.response.edit_message(embed=embed, view=None)
            except Exception as e:
                embed = Embed(
                    title="Error",
                    description="An error occurred while processing your disownment. Please try again later.",
                    color=embedColor["ERROR"]
                )
                await interaction.response.edit_message(embed=embed, view=None)
                return

        async def disownConfirmationDeclineCallback(interaction):
            if interaction.user.id != author_id:
                await interaction.response.send_message("You are not authorized to decline this disownment.", ephemeral=True)
                return

            embed = Embed(
                title="disown Cancelled",
                description=f"You have cancelled the disown from <@{selected_child_id}>.",
                color=embedColor["DEFAULT"]
            )
            await interaction.response.edit_message(embed=embed, view=None)

        disownConfirmationAcceptButton.callback = disownConfirmationAcceptCallback
        disownConfirmationDeclineButton.callback = disownConfirmationDeclineCallback

        disownConfirmationView.add_item(disownConfirmationAcceptButton)
        disownConfirmationView.add_item(disownConfirmationDeclineButton)

        await interaction.response.edit_message(embed=disownConfirmationEmbed, view=disownConfirmationView)

    disownSelectionView.add_item(disownSelectionDropdown)
    await ctx.send_message(embed=disownSelectionEmbed, view=disownSelectionView)