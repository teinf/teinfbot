import discord

from teinfbot.bot import TeinfBot
from teinfbot.db import db_session
from teinfbot.models import TeinfMember


async def on_message(msg: discord.Message):
    if msg.author.bot:
        return

    author_id: int = msg.author.id
    messageAuthor: TeinfMember = db_session.query(
        TeinfMember).filter_by(discordId=author_id).first()
    if messageAuthor:
        messageAuthor.sentmessages += 1
    else:
        member = TeinfMember(author_id)
        db_session.add(member)


def setup(bot: TeinfBot):
    bot.add_listener(on_message)
