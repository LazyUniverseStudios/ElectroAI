from discord import Embed
import discord
from asyncio import sleep

async def on_member_join(member):
    embed = Embed(title="Electro Cafe™", description=f"Welcome to our server, {member.mention}!", color=0x3b2dff)
    embed.set_thumbnail(url=member.avatar.url)
    embed.set_image(url="https://media.discordapp.net/attachments/1423660212866383975/1429399024170963064/F5x9UJSrN4b5Om60nZ1l.gif?ex=68f5ff14&is=68f4ad94&hm=cac1dee8f9b3d4d7c298ab5019871f483e59bd5fd23dcd58d8fc30707c2a6346&=&width=1000&height=556")
    embed.description="Post an introduction: <#1427499041775685732>\nCome chat with us: <#1412089191642431639>\n"
    embed.set_footer(text=f"We are now at {member.guild.member_count} members!")

    channel = member.guild.get_channel(1412087961205608691)
    await channel.send(member.mention, embed=embed)
    
    channel = member.guild.get_channel(1412089191642431639)
    await channel.send(member.mention, embed=embed)

    if not member.bot: 
        try:
            await member.send(member.mention, embed=embed)
        except discord.Forbidden:
            print(f"Could not send DM to {member.name}, they may have DMs disabled.")

    if member.bot:
        role = member.guild.get_role(1412101520786329711)
        await member.add_roles(role)
    
    if not member.bot:
        role = member.guild.get_role(1412101472438452306)
        await member.add_roles(role)
        await sleep(1)
        role = member.guild.get_role(1412101535227183176)
        await member.add_roles(role)
        await sleep(1)
        role = member.guild.get_role(1412101886001020929)
        await member.add_roles(role)
