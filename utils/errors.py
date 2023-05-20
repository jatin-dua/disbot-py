import discord
from discord.ext import commands

ERROR_MESSAGES = {
    commands.MissingRequiredArgument: "Missing command arguments.",
    commands.MissingPermissions: "You don't have the permission to use this command.",
    commands.MemberNotFound: "Member not found in the guild.",
}


def get_error_message(error: commands.CommandError, *, func: str) -> str:
    error_type = type(error)
    return ERROR_MESSAGES.get(
        error_type, "An error occurred while executing the command."
    )
