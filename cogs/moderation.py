import discord
from discord.ext import commands
from datetime import timedelta

SPAM_LIMIT = 4
TIME = timedelta(minutes=5.0)

class ModerationCog(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.message_count = {}
        self.previous_author_id = 0

    @commands.command(name='kick')
    async def kick_command(self, ctx: commands.Context, member: discord.Member, *, reason=None) -> None:
        if ctx.author.guild_permissions.kick_members:
            await member.kick(reason=reason)
            await ctx.reply(f"{member.mention} has been kicked from the server.")

        else:
            await ctx.reply("You do not have permission to kick members.")

    @commands.command(name='ban')
    async def ban_command(self, ctx: commands.Context, member: discord.Member, *, reason=None) -> None:
        if ctx.author.guild_permissions.ban_members:
            await member.ban(reason=reason)
            await ctx.reply(f'{member.mention} has been banned from the server.')

        else:
            await ctx.reply('You do not have permission to ban members.')

    @commands.command(name='mute')
    async def mute_command(self, ctx: commands.Context, member: discord.Member, *, reason=None) -> None: 
        if ctx.author.guild_permissions.mute_members:
            muted_role: discord.Role = discord.utils.get(ctx.guild.roles, name="muted")

            if not muted_role:
                muted_role = await ctx.guild.create_role(name="muted")
                for channel in ctx.guild.channels:
                    await channel.set_permissions(muted_role, send_messages=False)

            await member.add_roles(muted_role)
            await ctx.reply(f'{member.mention} has been muted .')

        else:
            await ctx.reply('You do not have permission to mute members.')

    @commands.command(name='unmute')
    async def unmute_command(self, ctx: commands.Context, member: discord.Member) -> None:
        muted_role: discord.Role = discord.utils.get(ctx.guild.roles, name="muted")

        if ctx.author.guild_permissions.mute_members:
            await member.remove_roles(muted_role)
            await ctx.reply(f'{member.mention} has been unmuted .')

        else:
            await ctx.reply('You do not have permission to unmute members.')

    async def check_message_flood(self, message: discord.Message) -> None:
        # print(f"""
        # Previous Author ID: {self.previous_author_id}
        
        # Message Author ID: {message.author.id}
        # Message Author: {message.author}
        #     """)
        
        self.message_count[message.author.id] = self.message_count.get(message.author.id, 1) + 1

        if self.previous_author_id != message.author.id:
            self.previous_author_id = message.author.id
            del self.message_count[self.previous_author_id]

        if self.message_count[message.author.id] > SPAM_LIMIT:
            # TODO: Store number of warns of each user and take action on them.
            await message.reply(f"{message.author.mention} Please refrain from flooding the channel with messages.")
            await message.author.timeout(TIME)


async def setup(client: commands.Bot):
    global MODERATOR
    MODERATOR = ModerationCog(client)
    await client.add_cog(MODERATOR)
