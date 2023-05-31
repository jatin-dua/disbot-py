import random
from typing import Any

import discord


def get_random_greeting() -> str:
    """Returns a random greeting string"""
    greetings = ["Hello", "Hi", "Hey there", "Greetings", "Salutations", "Howdy"]

    return random.choice(greetings)


def cembed(
    title: str | None = None,
    description: str | None = None,
    thumbnail: Any | None = None,
    picture: Any | None = None,
    url: Any | None = None,
    color: int | discord.Color = discord.Color.dark_theme(),
    footer: str | None = None,
    image: Any | None = None,
    fields: list[dict[str, Any]] | None = None,
) -> discord.Embed:
    """A helper function to create Discord embeds."""

    embed = discord.Embed()
    if color != discord.Color.dark_theme():
        if isinstance(color, str):
            color = int(color.replace("#", "0x"), base=16)
        embed = discord.Embed(color=color)

    if title:
        embed.title = title

    if description:
        embed.description = description

    if thumbnail:
        embed.set_thumbnail(url=thumbnail)

    if picture or image:
        embed.set_image(url=picture or image)

    if url:
        embed.url = url

    if footer:
        embed.set_footer(text=footer)

    if fields:
        for field in fields:
            embed.add_field(**field)

    return embed

def dict2str(d: dict):
    return "\n".join(f"`{i.upper()}: ` {j}" for i, j in d.items())

