import discord
from discord.ext import commands
from teinfbot.bot import TeinfBot
from teinfbot.db import db_session
from teinfbot.models import TeinfMember


async def on_message(msg: discord.Message):

    voting_channels_id = [816274528253771796, 816274319361048617]
    voting_emojis = ['🟩', '🟥', '🟨']

    if msg.channel.id in voting_channels_id:
        for emoji in voting_emojis:
            await msg.add_reaction(emoji)


def setup(bot: TeinfBot):
    bot.add_listener(on_message)
