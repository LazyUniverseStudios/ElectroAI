import discord
import asyncio

from discord import Embed, ButtonStyle, TextStyle
from discord.ui import Modal, TextInput, Button, View

from modules.confessions.db.set_Persistence import set_ConfessionPersistence

from modules.confessions.logic.random_CreateConfessionID import GenerateConfessionID
from modules.confessions.logic.dpy_CreateConfessionThread import create_ConfessionThread

from config import embedColor, channelIDs

global newthread

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

        confession_id = await GenerateConfessionID()

        # Post the confession embed
        confession_embed = Embed(
            title=f"Anonymous Confession #{confession_id}",
            description=confession_input.value,
            color=embedColor["CONFESSION"]
        )
        embed_footer_text = f"Confession ID: {confession_id}"
        confession_embed.set_footer(text=embed_footer_text)

        sentmsg = await confession_channel.send(embed=confession_embed)

        await create_ConfessionThread(
            message=sentmsg, 
            threadName=f"Discussion Thread for Confession #{confession_id}"
        )
        
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