""" This module contains methods for managing member roles."""
import discord
from discord.ext import commands

import utils.roles as roles
import utils.logger

logger = utils.logger.setup_logging(func=__name__)


class RoleCommands(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(name="addrole")
    async def add_role_command(
        self, ctx: commands.Context, member: discord.Member, role: str
    ) -> None:
        """
        Adds a role to the discord member.

        Parameters
        ----------
        ctx : commands.Context
            Represents the Command invocation context.

        member : discord.Member
            Represents a Discord member to a Guild.

        role : str
            Represents a Server role.
        """
        role = roles.get_role(ctx, role)

        if role is None:
            await ctx.reply(f"Oops! I cannot find the role you're asking for.")

        else:
            await member.add_roles(role)

    @commands.command(name="rmrole")
    async def remove_role_command(
        self, ctx: commands.Context, member: discord.Member, role: str
    ) -> None:
        """
        Removes a specified role from the discord member.

        Parameters
        ----------
        ctx : commands.Context
            Represents the Command invocation context.

        member : discord.Member
            Represents a Discord member to a Guild.

        role : str
            Represents a Server role.
        """
        role = roles.get_role(ctx, role)

        if role is None:
            await ctx.reply(f"Oops! I cannot find the role you're asking for.")
            return

        if role not in member.roles:
            await ctx.reply(f"{member.name} doesn't have the role specified.")

        else:
            await member.remove_roles(role)


async def setup(client: commands.Bot):
    await client.add_cog(RoleCommands(client))
