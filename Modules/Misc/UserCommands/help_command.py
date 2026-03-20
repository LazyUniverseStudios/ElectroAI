# Command In Progress - Do Not Use

import discord
from discord.ext import commands
from discord import Embed
from discord.ui import Button, View, Select, Modal, TextInput
from config import COMMAND_PREFIX, EmbedColor, EmbedColor_Error, EmbedColor_Success

@commands.command(name='help')
async def help_command(ctx, *, query: str = None):
    module_list = []
    command_list = []

    embed = Embed(color=EmbedColor)
    view = View()

    CommandSearchButton = Button(label="Search Commands", style=discord.ButtonStyle.green, custom_id="command_search_button")
    CommandSearchModal = Modal(title="Search Commands", custom_id="command_search_modal")
    CommandSearchInput = TextInput(label="Command Name", placeholder="Enter the command name you want to search for", required=True)
    CommandSearchModal.add_item(CommandSearchInput)
    async def CommandSearchButton_callback(interaction):
        await interaction.response.send_modal(CommandSearchModal)
    CommandSearchButton.callback = CommandSearchButton_callback

    ModuleSelectDropdown = Select(
        placeholder="Select a module to view its commands",
        options=[
            discord.SelectOption(label="Moderation", description="Commands for managing your server", value="moderation"),
            discord.SelectOption(label="Economy", description="Commands for the economy system", value="economy"),
            discord.SelectOption(label="Fun", description="Fun and games commands", value="fun"),
            discord.SelectOption(label="Utility", description="Useful utility commands", value="utility"),
            discord.SelectOption(label="Miscellaneous", description="Other commands that don't fit into a category", value="miscellaneous"),
        ],
        custom_id="module_select_dropdown",
    )

    if query is None:
        embed.title = "ElectroAI Help"
    await ctx.send(embed=embed)

