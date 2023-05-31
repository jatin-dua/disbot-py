""" This module is the entry point of the application."""
import asyncio

import discord
from discord.ext import commands

from config import TOKEN, COMMAND_PREFIX, EXTENSIONS
import utils.logger


async def main() -> None:
    """Entry point of the program."""
    try:
        logger = utils.logger.setup_logging(func=__name__)
        intents = discord.Intents.default()
        intents.message_content = True

        client = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

        # Load all extensions listed in the config
        success = 0
        total_extensions = len(EXTENSIONS)
        for extension in EXTENSIONS:
            try:
                await client.load_extension(extension)
                success += 1
                logger.info(f"Loaded {extension}")

            except Exception as e:
                logger.exception(e)

        logger.info(f"Loaded {success}/{total_extensions} extensions successfully")

        await client.start(TOKEN)

    except discord.errors.LoginFailure as error:
        logger.exception(error)

    finally:
        await client.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
