from typing import List

from discord.ext import tasks

from teinfbot.bot import TeinfBot
from teinfbot.db import db_session
from teinfbot.models import TeinfMember
from teinfbot.utils.members import MembersUtils


async def timeCounterStarter(bot: TeinfBot):
    await bot.wait_until_ready()
    timeCounter.start(bot)


@tasks.loop(minutes=1)
async def timeCounter(bot):
    onlineMembers = MembersUtils.get_online_members(bot)
    onlineMembersIds = [member.id for member in onlineMembers]
    onlineTeinfMembers: List[TeinfMember] = db_session.query(TeinfMember).filter(
        TeinfMember.discordId.in_(onlineMembersIds)).all()

    for onlineTeinfMember in onlineTeinfMembers:
        onlineTeinfMember.timespent += 1


def setup(bot: TeinfBot):
    bot.loop.create_task(timeCounterStarter(bot))
