import discord
from discord.ext import commands

ERROR_MESSAGES = {
    commands.MissingRequiredArgument: "Oops! Looks like you forgot to provide some required arguments.",
    commands.MissingPermissions: "You don't have the permission to use this command.",
    commands.MemberNotFound: "Sorry, but I couldn't find the specified member in the server."
}


def get_error_message(error: commands.CommandError) -> str:
    error_type = type(error)
    return ERROR_MESSAGES.get(
        error_type, "An error occurred while executing the command."
    )
