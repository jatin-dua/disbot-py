import discord
from discord.ext import commands
import utils.logger

logger = utils.logger.setup_logging(func=__name__)


class GeneralCog(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        await self.client.change_presence(activity=discord.Game("Chess"))
        logger.info(f"{self.client.user} is Online")

    @commands.command(name="info")
    async def botinfo(self, ctx: commands.Context) -> None:
        embed = discord.Embed(
            title="Bot Information",
            description="This bot was created by Jatin.",
            color=0x00FF00,
        )
        embed.set_thumbnail(url=self.client.user.avatar)
        embed.add_field(name="Bot Name", value=self.client.user.name, inline=True)
        embed.add_field(
            name="Bot Prefix", value=self.client.command_prefix, inline=True
        )
        embed.add_field(name="Bot ID", value=self.client.user.id, inline=False)
        embed.add_field(name="Server Count", value=len(self.client.guilds), inline=True)
        embed.add_field(name="User Count", value=len(self.client.users), inline=True)
        embed.set_footer(text=f"Powered by Discord.py v{discord.__version__}")
        await ctx.send(embed=embed)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(GeneralCog(client))
