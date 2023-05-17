# This requires the 'message_content' intent.
import discord
from discord.ext import commands
import asyncio
from config import TOKEN, COMMAND_PREFIX, EXTENSIONS

async def main() -> None:
    try:
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
                print(f"[ OK ] Loaded {extension}")
            
            except Exception as e:
                print(f"[ ERROR ] {e}")
        
        print(f"[ SUMMARY ] Loaded {success}/{total_extensions} extensions")

        await client.start(TOKEN)

    except discord.errors.LoginFailure as e:
        print(f"[ ERROR ] {e}")

    finally:
        await client.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

