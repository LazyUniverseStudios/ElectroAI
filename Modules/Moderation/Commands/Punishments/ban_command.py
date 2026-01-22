import discord

async def ban_command(ctx, target=discord.User.id | discord.User.name | discord.User.mention | None, *, reason=None):
    author = ctx.author
    
    if target == None:
        return
    elif target == discord.User.id:
        target = ctx.guild.me.get_user(target)