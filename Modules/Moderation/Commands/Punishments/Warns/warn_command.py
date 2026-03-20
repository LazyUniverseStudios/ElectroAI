import discord
from discord.ext import commands
from discord import embeds
from Modules.Moderation.Logic.create_caseid import GenerateCaseID
from InternalLogic.DatabaseLogic.DBQueries.DBQueries_Cases import CreateCase
from config import EmbedColor_Error, EmbedColor_Success

@commands.command(name="warn")
async def warn_command(ctx, target: discord.Member = None, *, reason=None):
    author = ctx.author
    bot = ctx.guild.me

    if bot.guild_permissions.manage_messages or bot.guild_permissions.administrator:
        pass
    else:
        embed = embeds.Embed(title="Error", description="I do not have permission to warn members.", color=EmbedColor_Error)
        await ctx.send(embed=embed)
        return

    if author.guild_permissions.manage_messages or author.guild_permissions.administrator:
        pass
    else:
        embed = embeds.Embed(title="Error", description="You do not have permission to warn members.", color=EmbedColor_Error)
        await ctx.send(embed=embed)
        return
    
    if target == None:
        embed = embeds.Embed(title="Error", description="Please specify a user to warn.", color=EmbedColor_Error)
        await ctx.send(embed=embed)
        return
    
    if reason == None:
        reason = "No reason provided."
    reason=f"Moderator: {author.name} ({author.id}) | Reason: {reason}"

    if isinstance(target, discord.Member):
        if bot.top_role <= target.top_role:
            embed = embeds.Embed(title="Error", description="I cannot warn this user because they have a higher or equal role than me.", color=EmbedColor_Error)
            await ctx.send(embed=embed)
            return
        
        if author.top_role <= target.top_role and author != ctx.guild.owner:
            embed = embeds.Embed(title="Error", description="You cannot warn this user because they have a higher or equal role than you.", color=EmbedColor_Error)
            await ctx.send(embed=embed)
            return
    
    if target == ctx.guild.owner:
        embed = embeds.Embed(title="Error", description="You cannot warn the server owner.", color=EmbedColor_Error)
        await ctx.send(embed=embed)
        return
    
    case_id = await GenerateCaseID()
    await CreateCase(case_id, "Warn", author.id, target.id, reason)
    embed = embeds.Embed(title="User Warned", description=f"{target.mention} has been warned.\n{reason}\nCase ID: {case_id}", color=EmbedColor_Success)
    await ctx.send(embed=embed)
    try:
        await target.send(f"You have been warned in {ctx.guild.name}\n{reason}. \nCaseID: {case_id}. Moderator: {author.name} ({author.id})")
    except:
        print(f"Unable to DM user {target.name} ({target.id}).")