import discord
from discord.ext import commands
from discord import embeds
from Modules.Moderation.Logic.create_caseid import GenerateCaseID
from InternalLogic.DatabaseLogic.DBQueries import CreateCase

@commands.command(name="untimeout", aliases=["um", "unmute"])
async def untimeout_command(ctx, target: discord.Member = None, *, reason=None):
    author = ctx.author
    bot = ctx.guild.me

    if bot.guild_permissions.moderate_members or bot.guild_permissions.administrator:
        pass
    else:
        embed = embeds.Embed(title="Error", description="I do not have permission to remove timeouts from members.", color=0xFF0000)
        await ctx.send(embed=embed)
        return
    
    if author.guild_permissions.moderate_members or author.guild_permissions.administrator:
        pass
    else:
        embed = embeds.Embed(title="Error", description="You do not have permission to remove timeouts from members.", color=0xFF0000)
        await ctx.send(embed=embed)
        return
    
    
    if target == None:
        embed = embeds.Embed(title="Error", description="Please specify a user to remove the timeout from.", color=0xFF0000)
        await ctx.send(embed=embed)
        return

    if target.timedout_until == None:
        embed = embeds.Embed(title="Error", description="I cannot remove the timeout from this user because they are not currently timed out.", color=0xFF0000)
        await ctx.send(embed=embed)
        return

    if reason == None:
        reason = "No reason provided."
    reason=f"Moderator: {author.name} ({author.id}) | Reason: {reason}"
    
    if isinstance(target, discord.Member):
        if bot.top_role <= target.top_role:
            embed = embeds.Embed(title="Error", description="I cannot remove the timeout from this user because they have a higher or equal role than me.", color=0xFF0000)
            await ctx.send(embed=embed)
            return
        
        if author.top_role <= target.top_role and author != ctx.guild.owner:
            embed = embeds.Embed(title="Error", description="You cannot remove the timeout from this user because they have a higher or equal role than you.", color=0xFF0000)
            await ctx.send(embed=embed)
            return
    
    if target == ctx.guild.owner:
        embed = embeds.Embed(title="Error", description="You cannot remove the timeout from the server owner because they cannot be timed out.", color=0xFF0000)
        await ctx.send(embed=embed)
        return
 
    try:
        await target.timeout(None, reason=reason)
        case_id = await GenerateCaseID()
        await CreateCase(case_id, "Untimeout", author.id, target.id, reason)
        embed = embeds.Embed(title="User Timeout Removed", description=f"{target.mention} has been removed from timeout.\n{reason}\nCase ID: {case_id}", color=0x00FF00)
        await ctx.send(embed=embed)
        try:
            await target.send(f"Your timeout has been removed in {ctx.guild.name}.\n{reason}. \nCaseID: {case_id}. Moderator: {author.name} ({author.id})")
        except:
            print(f"Unable to DM user {target.name} ({target.id}).")
    except Exception as e:
        embed = embeds.Embed(title="Error", description=f"An error occurred while trying to remove the timeout from the user: {str(e)}", color=0xFF0000)
        await ctx.send(embed=embed)
        return
