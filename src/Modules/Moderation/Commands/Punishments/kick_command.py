import discord
from discord.ext import commands
from discord import embeds
from Modules.Moderation.Logic.create_caseid import GenerateCaseID
from InternalLogic.DatabaseLogic.DBQueries.DBQueries_Cases import CreateCase
from config import EmbedColor_Error, EmbedColor_Success

@commands.command(name="kick")
async def kick_command(ctx, target: discord.Member = None, *, reason=None):
    author = ctx.author
    bot = ctx.guild.me

    if bot.guild_permissions.kick_members or bot.guild_permissions.administrator:
        pass
    else:
        embed = embeds.Embed(title="Error", description="I do not have permission to kick members.", color=EmbedColor_Error)
        await ctx.send(embed=embed)
        return
    
    if author.guild_permissions.kick_members or author.guild_permissions.administrator:
        pass
    else:
        embed = embeds.Embed(title="Error", description="You do not have permission to kick members.", color=EmbedColor_Error)
        await ctx.send(embed=embed)
        return
    
    
    if target == None:
        embed = embeds.Embed(title="Error", description="Please specify a user to kick.", color=EmbedColor_Error)
        await ctx.send(embed=embed)
        return

    if reason == None:
        reason = "No reason provided."
    reason=f"Moderator: {author.name} ({author.id}) | Reason: {reason}"
    
    if isinstance(target, discord.Member):
        if bot.top_role <= target.top_role:
            embed = embeds.Embed(title="Error", description="I cannot kick this user because they have a higher or equal role than me.", color=EmbedColor_Error)
            await ctx.send(embed=embed)
            return
        
        if author.top_role <= target.top_role and author != ctx.guild.owner:
            embed = embeds.Embed(title="Error", description="You cannot kick this user because they have a higher or equal role than you.", color=EmbedColor_Error)
            await ctx.send(embed=embed)
            return
    
    if target == ctx.guild.owner:
        embed = embeds.Embed(title="Error", description="You cannot kick the server owner.", color=EmbedColor_Error)
        await ctx.send(embed=embed)
        return
    
    try:
        await ctx.guild.kick(target, reason=reason)
        case_id = await GenerateCaseID()
        await CreateCase(case_id, "Kick", author.id, target.id, reason)
        embed = embeds.Embed(title="User Kicked", description=f"{target.mention} has been kicked.\n{reason}\nCase ID: {case_id}", color=EmbedColor_Success)
        await ctx.send(embed=embed)
        try:
            await target.send(f"You have been kicked from {ctx.guild.name}\n{reason}. \nCaseID: {case_id}. Moderator: {author.name} ({author.id})")
        except:
            print(f"Unable to DM user {target.name} ({target.id}).")
    except Exception as e:
        embed = embeds.Embed(title="Error", description=f"An error occurred while trying to kick the user: {str(e)}", color=EmbedColor_Error)
        await ctx.send(embed=embed)
        return
