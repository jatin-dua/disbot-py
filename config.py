from dotenv import load_dotenv
import os
import cogs

load_dotenv()

TOKEN: str = os.getenv('TOKEN')

COMMAND_PREFIX: str = '$'

# Extensions to load when starting up the bot
EXTENSIONS = [
    'cogs.general',
    'cogs.moderation'
]