import discord
from discord.ext import commands

from teinfbot.db import db_session
from teinfbot.models import TeinfMember
from teinfbot.utils.time import TimeUtils


@commands.command()
async def czas(ctx: commands.Context, member: discord.Member = None):
    await ctx.message.delete()

    member = member or ctx.message.author

    teinfMember: TeinfMember = db_session.query(TeinfMember).filter_by(discordId=member.id).first()

    em = discord.Embed(
        title="Czas spędzony na serwerze",
        description=f"{member.display_name} spędził {TimeUtils.getTimeDescFromMinutes(teinfMember.timespent)} na serwerze",
        color=discord.Colour.green()
    )
    await ctx.send(embed=em)


def setup(bot):
    bot.add_command(czas)
