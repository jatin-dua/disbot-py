""" This module contains the required config for the bot."""
import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

COMMAND_PREFIX = "$"

# Extensions to load when starting up the bot
EXTENSIONS = [
    "cogs.botinfo",
    "cogs.moderation",
    "cogs.message",
    "cogs.roles"
]
