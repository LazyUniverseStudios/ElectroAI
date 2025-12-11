from discord import Embed

async def on_member_remove(member):
    embed = Embed(title="Goodbye!", description=f"We're sad to see you go, {member.mention}.", color=0x6495ED)
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    embed.add_field(name="Farewell!", value="Thank you for being part of our community!", inline=False)
    embed.add_field(name="Stay Connected!", value="Feel free to rejoin us anytime!", inline=False)
    embed.set_footer(text=f"We are now at {member.guild.member_count} members.")
    
    channel = member.guild.get_channel(1412087983720632400)
    await channel.send(embed=embed)
