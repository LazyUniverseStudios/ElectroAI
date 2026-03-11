import discord
from discord.ext import commands
from discord import embeds
from Modules.Moderation.Logic.create_caseid import GenerateCaseID
from InternalLogic.DatabaseLogic.DBQueries import CreateCase

@commands.command(name="timeout", aliases=["tm", "mute"])
async def timeout_command(ctx, target: discord.Member = None, duration: int = None, *, reason=None):
    author = ctx.author
    bot = ctx.guild.me

    if bot.guild_permissions.moderate_members or bot.guild_permissions.administrator:
        pass
    else:
        embed = embeds.Embed(title="Error", description="I do not have permission to timeout members.", color=0xFF0000)
        await ctx.send(embed=embed)
        return
    
    if author.guild_permissions.moderate_members or author.guild_permissions.administrator:
        pass
    else:
        embed = embeds.Embed(title="Error", description="You do not have permission to timeout members.", color=0xFF0000)
        await ctx.send(embed=embed)
        return
    
    
    if target == None:
        embed = embeds.Embed(title="Error", description="Please specify a user to timeout.", color=0xFF0000)
        await ctx.send(embed=embed)
        return

    if duration == None:
        embed = embeds.Embed(title="Error", description="Please specify a duration for the timeout in minutes.", color=0xFF0000)
        await ctx.send(embed=embed)
        return

    if reason == None:
        reason = "No reason provided."
    reason=f"Moderator: {author.name} ({author.id}) | Reason: {reason}"
    
    if isinstance(target, discord.Member):
        if bot.top_role <= target.top_role:
            embed = embeds.Embed(title="Error", description="I cannot timeout this user because they have a higher or equal role than me.", color=0xFF0000)
            await ctx.send(embed=embed)
            return
        
        if author.top_role <= target.top_role and author != ctx.guild.owner:
            embed = embeds.Embed(title="Error", description="You cannot timeout this user because they have a higher or equal role than you.", color=0xFF0000)
            await ctx.send(embed=embed)
            return
    
    if target == ctx.guild.owner:
        embed = embeds.Embed(title="Error", description="You cannot timeout the server owner.", color=0xFF0000)
        await ctx.send(embed=embed)
        return

    try:
        await target.timeout(discord.utils.utcnow() + discord.timedelta(minutes=duration), reason=reason)
        case_id = await GenerateCaseID()
        await CreateCase(case_id, "Timeout", author.id, target.id, reason)
        embed = embeds.Embed(title="User Timed Out", description=f"{target.mention} has been timed out for {duration} minutes.\n{reason}\nCase ID: {case_id}", color=0x00FF00)
        await ctx.send(embed=embed)
        try:
            await target.send(f"You have been timed out in {ctx.guild.name} for {duration} minutes.\n{reason}. \nCaseID: {case_id}. Moderator: {author.name} ({author.id})")
        except:
            print(f"Unable to DM user {target.name} ({target.id}).")
    except Exception as e:
        embed = embeds.Embed(title="Error", description=f"An error occurred while trying to timeout the user: {str(e)}", color=0xFF0000)
        await ctx.send(embed=embed)
        return
