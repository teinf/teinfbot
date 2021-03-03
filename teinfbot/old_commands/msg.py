import discord
from discord.ext import commands

from teinfbot.bot import TeinfBot
from teinfbot.db import db_session
from teinfbot.models import TeinfMember


@commands.command()
async def msg(ctx: commands.Context, member: discord.Member = None):
    await ctx.message.delete()

    member = member or ctx.author
    messageAuthor: TeinfMember = db_session.query(TeinfMember).filter_by(discordId=member.id).first()

    em = discord.Embed(
        title="Wiadomości",
        description=f"Ilość wysłanych wiadomości przez {member.mention}\n**{messageAuthor.sentmessages}**",
        colour=discord.Colour.blue()
    )

    await ctx.channel.send(embed=em)


def setup(bot: TeinfBot):
    bot.add_command(msg)
