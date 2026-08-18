import discord

from discord.ext import commands

from config import embedColor

@commands.command(name="cry")
async def cry_command(ctx):
    """
    Sends a crying GIF in response to the command.

    Args:
        ctx: The context of the command.
    """
    # Fetch a crying GIF from Giphy
    try:
        from modules.emotes.logic.giphy_fetch import fetch_giphy_emote
        gif_url = await fetch_giphy_emote("anime crying")
    except Exception as e:
        await ctx.send(f"Error fetching crying GIF: {e}")
        return

    # Create an embed with the GIF
    embed = discord.Embed(
        title=f"{ctx.author.display_name} is crying!",
        color=embedColor["DEFAULT"]
    )
    embed.set_image(url=gif_url)

    # Send the embed in the channel
    await ctx.send(embed=embed)