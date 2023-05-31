""" This module contains methods for managing messages."""
import discord
from discord.ext import commands

class Messages(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    
    @commands.command(name="purge")
    async def purge_command(self, ctx: commands.Context, limit: int) -> None:
        """
        Purges the specified number of messages from a text channel.

        Parameters
        ----------
        ctx : commands.Context
            Represents the Command invocation context.

        limit : int
            Number of messages to purge.
        """
        if ctx.author.guild_permissions.manage_messages:
            await ctx.channel.purge(limit=limit)

            # TODO: Purge messages from specific user
            
            # messages = [message async for message in ctx.channel.history(limit=100) if message.author == member]
            # deleted = await ctx.channel.purge(limit=limit, check=lambda msg: msg in messages)
            # await ctx.channel.send(f"Deleted {len(deleted)} message(s)")

async def setup(client: commands.Bot):
    await client.add_cog(Messages(client))