from typing import List

import discord
from discord.ext import commands

from teinfbot.db import db_session
from teinfbot.models import TeinfMember
from teinfbot.utils.time import TimeUtils


@commands.command()
async def topka(ctx, amount: int = 10):
    await ctx.message.delete()

    topTimeSpentMembers: List[TeinfMember] = db_session.query(TeinfMember).order_by(TeinfMember.timespent).all()
    i = 1

    topkaTitle = "TOP CZASU"
    topkaDescription = ""

    for member in topTimeSpentMembers[::-1]:
        if i > amount:
            break

        mention = f"<@{member.discordId}>"

        topkaDescription += f"{i}. {mention:15} {TimeUtils.getTimeDescFromMinutes(member.timespent)}\n"
        i += 1

    em = discord.Embed(
        title=topkaTitle,
        description=topkaDescription,
        color=discord.Color.gold()
    )

    await ctx.send(embed=em)


def setup(bot):
    bot.add_command(topka)
