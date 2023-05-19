import discord
from discord.ext import commands

warns_count = {}
def get_warns(member_id: int) -> int:
    return warns_count.get(member_id, 0)

def add_warn(member_id: int) -> None:
    warns_count[member_id] = warns_count.get(member_id, 0) + 1