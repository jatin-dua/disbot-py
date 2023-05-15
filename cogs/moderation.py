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

    @commands.command(name='mute')
    async def mute_command(self, ctx: commands.Context, member: discord.Member, *, reason=None):
        if ctx.author.guild_permissions.mute_members:
            muted_role: discord.Role = discord.utils.get(ctx.guild.roles, name="muted")

            if not muted_role:
                muted_role = await ctx.guild.create_role(name="muted")
                for channel in ctx.guild.channels:
                    await channel.set_permissions(muted_role, send_messages=False)

            await member.add_roles(muted_role)
            await ctx.send(f'{member.mention} has been muted .')

        else:
            await ctx.send('You do not have permission to mute members.')

    @commands.command(name='unmute')
    async def unmute_command(self, ctx: commands.Context, member: discord.Member):
        muted_role: discord.Role = discord.utils.get(ctx.guild.roles, name="muted")

        if ctx.author.guild_permissions.mute_members:
            await member.remove_roles(muted_role)
            await ctx.send(f'{member.mention} has been unmuted .')

        else:
            await ctx.send('You do not have permission to unmute members.')


async def setup(client: commands.Bot):
    await client.add_cog(ModerationCog(client))
