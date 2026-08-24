import discord

from discord import Embed, ButtonStyle
from discord.ext import commands
from discord.ui import Button, View, Select

from config import embedColor

from modules.family.db.set_Partner import set_partner_divorce as set_partner
from modules.family.db.check_Spouse import check_spouse

@commands.command()
async def divorce(ctx):
    author_id = ctx.author.id

    spouseslist = await check_spouse(author_id)

    emptySlots = sum(1 for s in spouseslist if s is None)

    if emptySlots >= 2:
        embed = Embed(
            title="Error",
            description="You are not married to anyone.",
            color=embedColor["ERROR"]
        )
        await ctx.send(embed=embed)
        return

    divorceSelectionEmbed = Embed(
        title="Divorce",
        description="Please select the spouse you want to divorce from the dropdown menu below.",
        color=embedColor["DEFAULT"]
        )

    divorceSelectionView = View()

    divorceSelectionDropdown = Select(
        placeholder="Select a spouse to divorce",
        options=[
            discord.SelectOption(
                label=await ctx.bot.fetch_user(spouse_id).name, value=str(spouse_id)
                ) 
                for spouse_id in spouseslist if spouse_id is not None
                ]
    )

    divorceSelectionDropdown.callback = divorceSelectionCallback

    async def divorceSelectionCallback(interaction):
        if interaction.user.id != author_id:
            await interaction.response.send_message("You are not authorized to select a spouse for divorce.", ephemeral=True)
            return

        global selected_spouse_id
        selected_spouse_id = int(divorceSelectionDropdown.values[0])

        divorceConfirmationEmbed = Embed(
            title="Divorce Confirmation",
            description=f"Are you sure you want to divorce <@{selected_spouse_id}>?",
            color=embedColor["DEFAULT"]
        )

        divorceConfirmationView = View()

        divorceConfirmationAcceptButton = Button(
            label="Yes",
            style=ButtonStyle.green
        )

        divorceConfirmationDeclineButton = Button(
            label="No",
            style=ButtonStyle.red
        )

        async def divorceConfirmationAcceptCallback(interaction):
            if interaction.user.id != author_id:
                await interaction.response.send_message("You are not authorized to confirm this divorce.", ephemeral=True)
                return

            try:
                await set_partner(author_id, selected_spouse_id)
                embed = Embed(
                    title="Divorce Successful",
                    description=f"You have successfully divorced <@{selected_spouse_id}>.",
                    color=embedColor["SUCCESS"]
                )
                await interaction.response.edit_message(embed=embed, view=None)
            except Exception as e:
                embed = Embed(
                    title="Error",
                    description="An error occurred while processing your divorce. Please try again later.",
                    color=embedColor["ERROR"]
                )
                await interaction.response.edit_message(embed=embed, view=None)
                return

        async def divorceConfirmationDeclineCallback(interaction):
            if interaction.user.id != author_id:
                await interaction.response.send_message("You are not authorized to decline this divorce.", ephemeral=True)
                return

            embed = Embed(
                title="Divorce Cancelled",
                description=f"You have cancelled the divorce from <@{selected_spouse_id}>.",
                color=embedColor["DEFAULT"]
            )
            await interaction.response.edit_message(embed=embed, view=None)

        divorceConfirmationAcceptButton.callback = divorceConfirmationAcceptCallback
        divorceConfirmationDeclineButton.callback = divorceConfirmationDeclineCallback

        divorceConfirmationView.add_item(divorceConfirmationAcceptButton)
        divorceConfirmationView.add_item(divorceConfirmationDeclineButton)

        await interaction.response.edit_message(embed=divorceConfirmationEmbed, view=divorceConfirmationView)

    divorceSelectionView.add_item(divorceSelectionDropdown)
    await ctx.send_message(embed=divorceSelectionEmbed, view=divorceSelectionView)