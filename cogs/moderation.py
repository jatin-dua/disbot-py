""" This module contains methods for moderating members."""
from datetime import timedelta
import traceback

import discord
from discord.ext import commands

import utils.dtime
import utils.errors
import utils.logger
import utils.roles as roles

logger = utils.logger.setup_logging(func=__name__)

SPAM_LIMIT = 4
TIME = timedelta(minutes=10.0)
WARN_LIMIT = 2


class Moderation(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        self.message_count = {}
        self.warns_count = {}
        self.last_author_id = 0

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick_command(
        self,
        ctx: commands.Context,
        member: discord.Member,
        *,
        reason: str | None = None,
    ) -> None:
        """
        Kicks a member from the server.

        Parameters
        ----------
        ctx : commands.Context
            Represents the context in which a command is being invoked under.

        member : discord.Member
            Represents a Discord member to a Guild.

        reason : str | None, optional
            Represents the reason for kick, by default None
        """
        await member.kick(reason=reason)
        await ctx.reply(f"So long, {member.mention}! The exit doors are that way ➡️")

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban_command(
        self,
        ctx: commands.Context,
        member: discord.Member,
        *,
        reason: str | None = None,
    ) -> None:
        """
        Bans a member from the server.

        Parameters
        ----------
        ctx : commands.Context
            Represents the context in which a command is being invoked under.

        member : discord.Member
            Represents a Discord member to a Guild.

        reason : str | None, optional
            Represents the reason for ban, by default None
        """
        await member.ban(reason=reason)
        await ctx.reply(
            f"Say farewell to {member.mention}! They've been banished to the Shadow Realm. 👻"
        )

    @commands.command(name="mute")
    @commands.has_permissions(manage_roles=True)
    async def mute_command(self, ctx: commands.Context, member: discord.Member) -> None:
        """
        Mutes the member in the server.

        Parameters
        ----------
        ctx : commands.Context
            Represents the context in which a command is being invoked under.

        member : discord.Member
            Represents a Discord member to a Guild.
        """
        muted_role = roles.get_role(ctx, "muted")

        if muted_role is None:
            muted_role = await roles.create_role(
                ctx, role="muted", send_messages=False
            )

        await member.add_roles(muted_role)
        await ctx.reply(f"Shh! {member.mention} has been muted.")

    @commands.command(name="unmute")
    @commands.has_permissions(manage_roles=True)
    async def unmute_command(
        self, ctx: commands.Context, member: discord.Member
    ) -> None:
        """
        Unmutes the previously muted member.

        Parameters
        ----------
        ctx : commands.Context
            Represents the context in which a command is being invoked under.

        member : discord.Member
            Represents a Discord member to a Guild.
        """
        muted_role = roles.get_role(ctx, "muted")

        await member.remove_roles(muted_role)
        await ctx.reply(f"Breaking the silence! {member.mention} has been unmuted.")

    @commands.command(name="timeout")
    @commands.has_permissions(moderate_members=True)
    async def timeout_command(
        self, ctx: commands.Context, member: discord.Member, time: str
    ) -> None:
        """
        Applies a time out to a member for the given time.

        Parameters
        ----------
        ctx : commands.Context
            Represents the context in which a command is being invoked under.

        member : discord.Member
            Represents a Discord member to a Guild.

        time : str
            Represents the time for timeout.
        """
        await member.timeout(utils.dtime.parse_time(time))
        await ctx.reply(
            f"Timeout in effect for {member.mention}. Take a break from the server!"
        )

    @commands.command(name="warn")
    @commands.has_permissions(moderate_members=True)
    async def warn_command(self, ctx: commands.Context, member: discord.Member) -> None:
        """
        Warns the member for inappropriate action.

        Parameters
        ----------
        ctx : commands.Context
            Represents the context in which a command is being invoked under.

        member : discord.Member
            Represents a Discord member to a Guild.
        """
        self.add_warn(member.id)
        warns = self.get_warns(member.id)
        print(f"{member.name} has {warns} warn(s).")

        if warns == WARN_LIMIT:
            await ctx.reply(
                f"So long, {member.mention}! The exit doors are that way ➡️"
            )
            await member.kick()
            return

        await ctx.reply(
            f"{member.mention} Show good manners and treat others as you would like to be treated."
        )
        await member.timeout(TIME)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        """
        Event triggered when a message is sent in server.

        Parameters
        ----------
        message : discord.Message
            Represents a message from Discord.
        """
        if message.author == self.client.user:
            return

        await self.check_message_flood(message)

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        """
        Event triggered when a command raises an exception.

        Parameters
        ----------
        ctx : commands.Context
            The invocation context.

        error : commands.CommandError
            The Error that was raised.
        """
        command_name = ctx.command.name if ctx.command else "unknown"
        error_traceback = "".join(
            traceback.format_exception(type(error), error, error.__traceback__)
        )
        logger.error(f"[command '{command_name}']: {error} \n{error_traceback}")
        await ctx.reply(utils.errors.get_error_message(error))

    async def check_message_flood(self, message: discord.Message) -> None:
        """
        Checks if the channel is flooded with messages by a member, and take action.

        Parameters
        ----------
        message : discord.Message
            Represents a message from Discord.
        """
        author_id = message.author.id
        self.add_message_count(author_id)
        if self.last_author_id != author_id:
            self.last_author_id = author_id
            self.clear_message_count(self.last_author_id)

        if self.message_count[author_id] == SPAM_LIMIT:
            self.clear_message_count(author_id)
            await message.reply(
                f"Too many messages, too little time! Timeout initiated for {message.author.mention}."
            )
            await message.author.timeout(TIME)

    def get_warns(self, member_id: int) -> int:
        return self.warns_count.get(member_id, 0)

    def add_warn(self, member_id: int) -> None:
        self.warns_count[member_id] = self.warns_count.get(member_id, 0) + 1

    def add_message_count(self, member_id: int) -> None:
        self.message_count[member_id] = self.message_count.get(member_id, 0) + 1

    def clear_message_count(self, member_id: int) -> None:
        del self.message_count[member_id]


async def setup(client: commands.Bot):
    await client.add_cog(Moderation(client))
