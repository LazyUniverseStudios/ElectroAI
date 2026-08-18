import discord

from discord import Embed, ButtonStyle, TextStyle
from discord.ui import Modal, TextInput, Button, View

from modules.confessions.db.set_Persistence import set_ConfessionPersistence

from config import embedColor, channelIDs


async def sendConfessionModalMessage(bot):
    channel = bot.get_channel(channelIDs["CONFESSIONS_CHANNEL"]) or await bot.fetch_channel(channelIDs["CONFESSIONS_CHANNEL"])

    submitMsgEmbed = Embed(
        title="Submit an Anonymous Confession!",
        description="Press the button below to submit an anonymous confession into this channel!",
        color=embedColor["DEFAULT"]
    )

    submitConfessionButton = Button(
        style=ButtonStyle.primary,
        label="Submit a Confession",
        emoji="🤫",
        custom_id="submit_confession_btn"
    )

    # Pass the function reference (do not invoke it here)
    submitConfessionButton.callback = confessionButtonCallback

    submitMsgView = View(timeout=None)
    submitMsgView.add_item(submitConfessionButton)

    # Send the sticky prompt and update persistence in DB
    sent_msg = await channel.send(embed=submitMsgEmbed, view=submitMsgView)
    await set_ConfessionPersistence(sent_msg.id)
    return sent_msg


async def confessionButtonCallback(interaction: discord.Interaction):
    # 1. Build the Modal and TextInput without class definitions
    confession_modal = Modal(title="Anonymous Confession")
    
    confession_input = TextInput(
        label="Your Confession",
        style=TextStyle.paragraph,
        placeholder="Type your confession here...",
        max_length=2000,
        required=True
    )
    confession_modal.add_item(confession_input)

    # 2. Define the modal submission callback
    async def modal_submit_callback(modal_interaction: discord.Interaction):
        # Acknowledge ephemerally first so only the submitter sees this
        await modal_interaction.response.send_message("Your confession has been sent anonymously!", ephemeral=True)

        confession_channel = modal_interaction.guild.get_channel(channelIDs["CONFESSIONS_CHANNEL"])
        if not confession_channel:
            return

        # Post the confession embed
        confession_embed = Embed(
            title="Anonymous Confession",
            description=confession_input.value,
            color=embedColor["CONFESSION"]
        )
        await confession_channel.send(embed=confession_embed)

        # Delete the previous sticky message (the one clicked)
        try:
            await interaction.message.delete()
        except (discord.NotFound, discord.HTTPException):
            pass

        # Resend a fresh sticky prompt to stay at the bottom & save its new ID
        await sendConfessionModalMessage(modal_interaction.client)

    # Attach the callback dynamically to the modal
    confession_modal.on_submit = modal_submit_callback

    # 3. Present the modal to the user
    await interaction.response.send_modal(confession_modal)