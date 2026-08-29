import discord

from discord import Embed, ButtonStyle
from discord.ext import commands
from discord.ui import Button, View

from config import embedColor

from modules.family.db.check_Parent import check_parent
from modules.family.db.check_Children import check_children
from modules.family.db.set_Child import set_child_adoption as set_child
from modules.family.db.set_Parent import set_parent

@commands.command()
async def makeparent(ctx, target: discord.Member = None):
    if target is None:
        embed = Embed(
            title="Error: No Member Provided",
            description="Please specify a user to make your parent.",
            color=embedColor["ERROR"]
        )
        await ctx.send(embed=embed)
        return

    if target == ctx.author:
        embed = Embed(
            title="Error: Target cannot be Self",
            description="You cannot make yourself your own parent.",
            color=embedColor["ERROR"]
        )
        await ctx.send(embed=embed)
        return

    author_id = ctx.author.id
    target_id = target.id

    parent = await check_parent(author_id)

    if parent[0] == True:
        if parent[1] == target_id:
            embed = Embed(
                title="Error: Already Parent of Target",
                description=f"{target.mention} is already your parent.",
                color=embedColor["ERROR"]
            )
            await ctx.send(embed=embed)
            return
        else:
            embed = Embed(
                title="Error: You Already Have a Parent",
                description=f"You already have a parent. You cannot have multiple parents.",
                color=embedColor["ERROR"]
            )
            await ctx.send(embed=embed)
            return

    target_children = await check_children(target_id)

    children_count = 0
    for child_id in target_children:
        if child_id is not None:
            children_count += 1

    if children_count >= 6:
        embed = Embed(
            title="Error: Maximum Children Reached",
            description="The user you are trying to make your parent already has 6 children.",
            color=embedColor["ERROR"]
        )
        embed.set_footer(text=f".adopt")
        await ctx.send(embed=embed)
        return

    makeparent_slot = target_children.index(None) + 1

    makeparentStage1Embed = Embed(
        title="makeparent Request",
        description=f"Are you sure you want to have {target.mention} as your parent?",
        color=embedColor["DEFAULT"]
    )
    makeparentStage1View = View()

    async def makeparentStage1ConfirmCallback(interaction):
        if interaction.user.id != author_id:
            await interaction.response.send_message("You are not authorized to confirm this makeparent.", ephemeral=True)
            return

        makeparentStage2Embed = Embed(
            title="makeparent Request",
            description=f"Hey <@{target_id}>, {ctx.author.mention} wants to adopt you! Do you accept?",
            color=embedColor["DEFAULT"]
        )

        async def makeparentStage2AcceptCallback(interaction):
            if interaction.user.id != target_id:
                await interaction.response.send_message("You are not authorized to accept this makeparent.", ephemeral=True)
                return

            # Update the database to set the parent-child relationship
            try:
                await set_child(target_id, author_id, makeparent_slot)
                await set_parent(target_id, author_id)
                embed = Embed(
                                title="makeparent Accepted",
                                description=f"Welcome to the family, <@{target_id}>! You are now the child of <@{author_id}>.",
                                color=embedColor["SUCCESS"]
                            )
                await interaction.response.edit_message(embed=embed, view=None)
            except Exception as e:
                print(f"Error occurred while setting child: {e}")
                embed = Embed(
                    title="Error: Unable to Reach Database",
                    description="An error occurred while processing the makeparent. Please try again later.",
                    color=embedColor["ERROR"]
                )
                await interaction.response.edit_message(embed=embed, view=None)

        async def makeparentStage2DeclineCallback(interaction):
            if interaction.user.id != target_id:
                await interaction.response.send_message("You are not authorized to decline this makeparent.", ephemeral=True)
                return

            embed = Embed(
                title="makeparent Declined",
                description=f"Sorry <@{author_id}>, <@{target_id}> has declined your makeparent request.",
                color=embedColor["ERROR"]
            )
            await interaction.response.edit_message(embed=embed, view=None)

        makeparentStage2View = View()

        makeparentStage2AcceptButton = Button(label="Accept", style=ButtonStyle.green)
        makeparentStage2AcceptButton.callback = makeparentStage2AcceptCallback
        
        makeparentStage2DeclineButton = Button(label="Decline", style=ButtonStyle.red)
        makeparentStage2DeclineButton.callback = makeparentStage2DeclineCallback

        makeparentStage2View.add_item(makeparentStage2AcceptButton)
        makeparentStage2View.add_item(makeparentStage2DeclineButton)

        await interaction.response.edit_message(embed=makeparentStage2Embed, view=makeparentStage2View)


    async def makeparentStage1CancelCallback(interaction):
        if interaction.user.id != author_id:
            await interaction.response.send_message("You are not authorized to cancel this makeparent.", ephemeral=True)
            return

        makeparentStage1CancelEmbed = Embed(
            title="makeparent Cancelled",
            description=f"You have cancelled the makeparent of {target.mention}.",
            color=embedColor["ERROR"]
        )
        await interaction.response.edit_message(embed=makeparentStage1CancelEmbed, view=None)

    makeparentStage1ConfirmButton = Button(label="Confirm", style=ButtonStyle.green)
    makeparentStage1ConfirmButton.callback = makeparentStage1ConfirmCallback

    makeparentStage1CancelButton = Button(label="Cancel", style=ButtonStyle.red)
    makeparentStage1CancelButton.callback = makeparentStage1CancelCallback

    makeparentStage1View.add_item(makeparentStage1ConfirmButton)
    makeparentStage1View.add_item(makeparentStage1CancelButton)

    await ctx.send(embed=makeparentStage1Embed, view=makeparentStage1View)