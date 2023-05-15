import discord
from discord.ext import commands

class ModerationCog(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(name='kick')
    async def kick_command(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author.guild_permissions.kick_members:
            await member.kick(reason=reason)
            await ctx.send(f'{member.mention} has been kicked from the server.')

        else:
            await ctx.send('You do not have permission to kick members.')

    @commands.command(name='ban')
    async def ban_command(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author.guild_permissions.ban_members:
            await member.ban(reason=reason)
            await ctx.send(f'{member.mention} has been banned from the server.')

        else:
            await ctx.send('You do not have permission to ban members.')

async def setup(client: commands.Bot):
    await client.add_cog(ModerationCog(client))
