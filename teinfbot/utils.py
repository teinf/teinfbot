import discord
from discord.ext import commands, tasks
import random
from typing import List, Tuple


def is_private_channel(channel: discord.TextChannel):
    return str(channel.type) == "private"


def get_digits(amount=9):
    digs: List[str] = [str(i) + "\u20e3" for i in range(1, 10)]

    for digit in digs[:amount]:
        yield digit


def get_emoji_value(emoji: discord.Emoji) -> int:
    digs: List[str] = [str(i) + "\u20e3" for i in range(1, 10)]
    return digs.index(str(emoji)) + 1


async def add_digits(msg: discord.Message, amount: int):
    for emoji in get_digits(amount):
        await msg.add_reaction(emoji)
