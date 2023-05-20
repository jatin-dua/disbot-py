import discord
from discord.ext import commands
from cogs.moderation import MODERATOR
import utils.logger
import utils.errors
import traceback

logger = utils.logger.setup_logging(func=__name__)


class EventHandlerCog(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.client.user:
            return

        await MODERATOR.check_message_flood(message)

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        command_name = ctx.command.name if ctx.command else "unknown"
        error_traceback = "".join(
            traceback.format_exception(type(error), error, error.__traceback__)
        )
        logger.error(f"[command '{command_name}']: {error} \n{error_traceback}")
        await ctx.reply(utils.errors.get_error_message(error))

    # @commands.Cog.listener()
    # async def on_member_join(self, member: discord.Member):
    #     if (discord.utils.utcnow() - member.created_at).days < 1:
    #         await member.kick(reason='New account.')
    #         mod_channel = self.client.get_channel(1234567890) # Replace with your moderation channel ID
    #         await mod_channel.send(f"Suspicious account {member.mention} has joined the server.")


async def setup(client: commands.Bot):
    await client.add_cog(EventHandlerCog(client))
