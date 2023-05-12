# This requires the 'message_content' intent.
import discord
from discord.ext import commands
import asyncio
from config import TOKEN, COMMAND_PREFIX, EXTENSIONS

async def main():
    try:
        intents = discord.Intents.default()
        intents.message_content = True

        client = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

        # Load all extensions listed in the config
        for extension in EXTENSIONS:
            await client.load_extension(extension)

        await client.start(TOKEN)

    except discord.errors.LoginFailure:
        print(f"Invalid Bot Token: {TOKEN}")

    finally:
        await client.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

