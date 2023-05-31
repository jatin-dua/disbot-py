import traceback

import discord
from discord.ext import commands

import utils.errors as errors
import utils.logger

logger = utils.logger.setup_logging(func=__name__)

class ErrorHandler(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
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
        await ctx.reply(errors.get_error_message(error))

async def setup(client: commands.Bot):
    await client.add_cog(ErrorHandler(client))
