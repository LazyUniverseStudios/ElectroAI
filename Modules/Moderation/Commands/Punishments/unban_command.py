import discord
from discord.ext import commands
from discord import embeds
from Modules.Moderation.Logic.create_caseid import GenerateCaseID
from InternalLogic.DatabaseLogic.DBQueries import CreateCase

@commands.command(name="unban", aliases=["ub"])
async def unban_command(ctx, target: discord.User = None, *, reason=None):
    author = ctx.author
    bot = ctx.guild.me

    if bot.guild_permissions.ban_members or bot.guild_permissions.administrator:
        pass
    else:
        embed = embeds.Embed(title="Error", description="I do not have permission to unban members.", color=0xFF0000)
        await ctx.send(embed=embed)
        return
    if author.guild_permissions.ban_members or author.guild_permissions.administrator:
        pass
    else:
        embed = embeds.Embed(title="Error", description="You do not have permission to unban members.", color=0xFF0000)
        await ctx.send(embed=embed)
        return
    
    
    if target == None:
        embed = embeds.Embed(title="Error", description="Please specify a user to unban.", color=0xFF0000)
        await ctx.send(embed=embed)
        return
    
    try:
        await ctx.guild.fetch_ban(target)
    except discord.NotFound:
        embed = embeds.Embed(title="Error", description="That user is not currently banned.", color=0xFF0000)
        await ctx.send(embed=embed)
        return

    if reason == None:
        reason = "No reason provided."
    reason=f"Moderator: {author.name} ({author.id}) | Reason: {reason}"
    
    try:
        await ctx.guild.unban(target, reason=reason)
        case_id = await GenerateCaseID()
        await CreateCase(case_id, "Unban", author.id, target.id, reason)
        embed = embeds.Embed(title="User Unbanned", description=f"{target.mention} has been unbanned.\n{reason}\nCase ID: {case_id}", color=0x00FF00)
        await ctx.send(embed=embed)
        try:
            await target.send(f"You have been unbanned from {ctx.guild.name}\n{reason}. \nCaseID: {case_id}. Moderator: {author.name} ({author.id})")
        except:
            print(f"Unable to DM user {target.name} ({target.id}).")
    except Exception as e:
        embed = embeds.Embed(title="Error", description=f"An error occurred while trying to unban the user: {str(e)}", color=0xFF0000)
        await ctx.send(embed=embed)
        return
