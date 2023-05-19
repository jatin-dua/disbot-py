import discord
from discord.ext import commands
from datetime import timedelta
import utils.dtime
import utils.errors

SPAM_LIMIT = 4
TIME = timedelta(minutes=5.0)


class ModerationCog(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        self.message_count = {}
        self.last_author_id = 0

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick_command(
        self, ctx: commands.Context, member: discord.Member, *, reason=None
    ) -> None:
        await member.kick(reason=reason)
        await ctx.reply(f"So long, {member.mention}! The exit doors are that way ➡️")

    @kick_command.error
    async def kick_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        await ctx.reply(utils.errors.get_error_message(error, func=__name__))

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban_command(
        self, ctx: commands.Context, member: discord.Member, *, reason=None
    ) -> None:
        await member.ban(reason=reason)
        await ctx.reply(
            f"Say farewell to {member.mention}! They've been banished to the Shadow Realm. 👻"
        )

    @ban_command.error
    async def ban_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        await ctx.reply(utils.errors.get_error_message(error, func=__name__))

    @commands.command(name="mute")
    @commands.has_permissions(manage_roles=True)
    async def mute_command(self, ctx: commands.Context, member: discord.Member) -> None:
        muted_role: discord.Role = discord.utils.get(ctx.guild.roles, name="muted")

        if not muted_role:
            muted_role = await ctx.guild.create_role(name="muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, send_messages=False)

        await member.add_roles(muted_role)
        await ctx.reply(f"Shh! {member.mention} has been muted.")

    @mute_command.error
    async def mute_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        await ctx.reply(utils.errors.get_error_message(error, func=__name__))

    @commands.command(name="unmute")
    @commands.has_permissions(manage_roles=True)
    async def unmute_command(
        self, ctx: commands.Context, member: discord.Member
    ) -> None:
        muted_role: discord.Role = discord.utils.get(ctx.guild.roles, name="muted")

        await member.remove_roles(muted_role)
        await ctx.reply(f"Breaking the silence! {member.mention} has been unmuted.")

    @unmute_command.error
    async def unmute_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        await ctx.reply(utils.errors.get_error_message(error, func=__name__))

    @commands.command(name="timeout")
    @commands.has_permissions(moderate_members=True)
    async def timeout_command(
        self, ctx: commands.Context, member: discord.Member, time: str
    ) -> None:
        await member.timeout(utils.dtime.parse_time(time))
        await ctx.reply(
            f"Oh no, {member.mention} is in timeout! Think about your actions and reflect on the server rules."
        )

    @timeout_command.error
    async def timeout_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        await ctx.reply(utils.errors.get_error_message(error, func=__name__))

    async def check_message_flood(self, message: discord.Message) -> None:
        self.message_count[message.author.id] = (
            self.message_count.get(message.author.id, 1) + 1
        )

        if self.last_author_id != message.author.id:
            self.last_author_id = message.author.id
            del self.message_count[self.last_author_id]

        if self.message_count[message.author.id] > SPAM_LIMIT:
            # TODO: Store number of warns of each user and take action on them.
            await message.reply(
                f"Too many messages, too little time! Timeout initiated for {message.author.mention}. See you on the other side!"
            )
            await message.author.timeout(TIME)


async def setup(client: commands.Bot):
    global MODERATOR
    MODERATOR = ModerationCog(client)
    await client.add_cog(MODERATOR)
