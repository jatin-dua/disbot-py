""" This module contains methods for related to the Bot Information."""
from time import time
from typing import Coroutine

import discord
from discord.ext import commands

import utils.logger
import utils.response
from config import COMMAND_PREFIX

logger = utils.logger.setup_logging(func=__name__)


class BotInfo(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @staticmethod
    async def timed(coro: Coroutine) -> tuple:
        """Time the execution of a coroutine."""

        start = time()
        result = await coro
        end = time()

        return (result, f"{(end - start) * 1000:.2f}ms")

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """
        Event triggered when the bot is ready for acrion.
        """
        await self.client.change_presence(activity=discord.Game("Chess"))
        logger.info(f"{self.client.user} is now Online.")

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

        if f"<@{self.client.user.id}>" in message.content:
            # TODO: Implement a custom command prefix

            prefi = COMMAND_PREFIX
            embed = utils.response.cembed(
                title=f"Hi there! I am {(self.client.user.name).title()}.",
                description=f"""Prefix is `{prefi}`\nFor more help, type `{prefi}help`""",
                thumbnail=self.client.user.avatar,
            )

            await message.channel.send(embed=embed)

    @commands.command(name="info")
    async def info_command(self, ctx: commands.Context) -> None:
        """
        Display the bot information.

        Parameters
        ----------
        ctx : commands.Context
            Represents the Command invocation context.
        """
        fields = [
            {
                "name": "Name", 
                "value": self.client.user.name, 
                "inline": True
            },
            {
                "name": "Prefix", 
                "value": self.client.command_prefix, 
                "inline": True
            },
            {
                "name": "Server Count", 
                "value": len(self.client.guilds), 
                "inline": False
            }
        ]

        embed = utils.response.cembed(
            title="Bot Information",
            description=f"Hi there! I am {(self.client.user.name).title()}.",
            thumbnail=self.client.user.avatar,
            footer=f"Powered by Discord.py v{discord.__version__}",
            fields=fields,
        )

        await ctx.send(embed=embed)

    @commands.command(name="ping")
    async def ping_command(self, ctx: commands.Context) -> None:
        """
        Get the bot's websocket and HTTP ping.

        Parameters
        ----------
        ctx : commands.Context
            Represents the Command invocation context.
        """

        send = await self.timed(ctx.send("Testing ping..."))
        message = send[0]
        edit = await self.timed(message.edit(content="Testing editing..."))
        delete = await self.timed(message.delete())

        result_fields = [
            {
                "name": "🌐 WebSocket latency",
                "value": f"{self.client.latency * 1000:.2f}ms",
                "inline": False,
            },
            {
                "name": "▶️ Message Send", 
                "value": send[1], 
                "inline": False
            },
            {
                "name": "🔄 Message Edit", 
                "value": edit[1], 
                "inline": False},
            {
                "name": "🚫 Message Delete", 
                "value": delete[1], 
                "inline": False
            }
        ]

        results = utils.response.cembed(
            color=0x87CEEB, title="Ping Stats", thumbnail=self.client.user.avatar, fields=result_fields
        )

        await ctx.send(embed=results)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(BotInfo(client))
