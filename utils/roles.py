import discord
from discord.ext import commands

async def create_role(ctx: commands.Context, role: str, **permissions: bool | None) -> discord.Role | None:
    new_role = await ctx.guild.create_role(name=role)
    for channel in ctx.guild.channels:
        await channel.set_permissions(new_role, **permissions)
    return get_role(ctx, role=role)

def get_role(ctx: commands.Context, role: str) -> discord.Role | None:
    return discord.utils.get(ctx.guild.roles, name=role)