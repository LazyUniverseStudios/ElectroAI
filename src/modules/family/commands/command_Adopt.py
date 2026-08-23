import discord

from discord import Embed, ButtonStyle
from discord.ext import commands
from discord.ui import Button, View

from config import embedColor

from modules.family.db.check_Parent import check_parent
from modules.family.db.check_Children import check_children
from modules.family.db.set_Child import set_child

@commands.command()
async def adopt(ctx, member: discord.Member = None):
    if member is None:
        embed = Embed(
            title="Error",
            description="Please specify a member to adopt.",
            color=embedColor["ERROR"]
        )
        await ctx.send(embed=embed)
        return

    if member == ctx.author:
        embed = Embed(
            title="Error",
            description="You cannot adopt yourself.",
            color=embedColor["ERROR"]
        )
        await ctx.send(embed=embed)
        return

    author_id = ctx.author.id
    target_id = member.id

    parent = await check_parent(target_id)

    if parent[0] == True:
        if parent[1] == author_id:
            embed = Embed(
                title="Error",
                description=f"You are already the parent of {member.mention}.",
                color=embedColor["ERROR"]
            )
            await ctx.send(embed=embed)
            return
        else:
            embed = Embed(
                title="Error",
                description=f"{member.mention} already has a parent.",
                color=embedColor["ERROR"]
            )
            await ctx.send(embed=embed)
            return

    current_children = await check_children(author_id)

    children_count = 0
    for child_id in current_children:
        if child_id is not None:
            children_count += 1

    if children_count >= 6:
        embed = Embed(
            title="Error",
            description="You cannot adopt more than 6 children.",
            color=embedColor["ERROR"]
        )
        await ctx.send(embed=embed)
        return

    adoption_slot = current_children.index(None) + 1

    adoptionStage1Embed = Embed(
        title="Adoption Request",
        description=f"Are you sure you want to adopt {member.mention} as your child?",
        color=embedColor["DEFAULT"]
    )
    adoptionStage1View = View()

    async def adoptionStage1ConfirmCallback(interaction):
        if interaction.user.id != author_id:
            await interaction.response.send_message("You are not authorized to confirm this adoption.", ephemeral=True)
            return

        adoptionStage2Embed = Embed(
            title="Adoption Request",
            description=f"Hey <@{target_id}>, {ctx.author.mention} wants to adopt you! Do you accept?",
            color=embedColor["DEFAULT"]
        )

        async def adoptionStage2AcceptCallback(interaction):
            if interaction.user.id != target_id:
                await interaction.response.send_message("You are not authorized to accept this adoption.", ephemeral=True)
                return

            # Update the database to set the parent-child relationship
            try:
                await set_child(author_id, target_id, adoption_slot)
                embed = Embed(
                                title="Adoption Accepted",
                                description=f"Welcome to the family, <@{target_id}>! You are now the child of <@{author_id}>.",
                                color=embedColor["SUCCESS"]
                            )
                await interaction.response.send_message(embed=embed, view=None)
            except Exception as e:
                print(f"Error occurred while setting child: {e}")
                embed = Embed(
                    title="Error",
                    description="An error occurred while processing the adoption. Please try again later.",
                    color=embedColor["ERROR"]
                )
                await interaction.response.send_message(embed=embed, view=None)

        async def adoptionStage2DeclineCallback(interaction):
            if interaction.user.id != target_id:
                await interaction.response.send_message("You are not authorized to decline this adoption.", ephemeral=True)
                return

            embed = Embed(
                title="Adoption Declined",
                description=f"Sorry <@{author_id}>, <@{target_id}> has declined your adoption request.",
                color=embedColor["ERROR"]
            )
            await interaction.response.send_message(embed=embed, view=None)

        adoptionStage2View = View()

        adoptionStage2AcceptButton = Button(label="Accept", style=ButtonStyle.green)
        adoptionStage2AcceptButton.callback = adoptionStage2AcceptCallback
        
        adoptionStage2DeclineButton = Button(label="Decline", style=ButtonStyle.red)
        adoptionStage2DeclineButton.callback = adoptionStage2DeclineCallback

        adoptionStage2View.add_item(adoptionStage2AcceptButton)
        adoptionStage2View.add_item(adoptionStage2DeclineButton)

        await interaction.response.send_message(embed=adoptionStage2Embed, view=adoptionStage2View)


    async def adoptionStage1CancelCallback(interaction):
        if interaction.user.id != author_id:
            await interaction.response.send_message("You are not authorized to cancel this adoption.", ephemeral=True)
            return

        adoptionStage1CancelEmbed = Embed(
            title="Adoption Cancelled",
            description=f"You have cancelled the adoption of {member.mention}.",
            color=embedColor["ERROR"]
        )
        await interaction.response.send_message(embed=adoptionStage1CancelEmbed, view=None)

    adoptionStage1ConfirmButton = Button(label="Confirm", style=ButtonStyle.green)
    adoptionStage1ConfirmButton.callback = adoptionStage1ConfirmCallback

    adoptionStage1CancelButton = Button(label="Cancel", style=ButtonStyle.red)
    adoptionStage1CancelButton.callback = adoptionStage1CancelCallback

    adoptionStage1View.add_item(adoptionStage1ConfirmButton)
    adoptionStage1View.add_item(adoptionStage1CancelButton)

    await ctx.send(embed=adoptionStage1Embed, view=adoptionStage1View)
