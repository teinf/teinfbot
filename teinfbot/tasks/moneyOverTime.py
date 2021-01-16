from typing import List

from discord.ext import commands, tasks
from teinfbot import TeinfBot, db_session
import asyncio

from teinfbot.models import TeinfMember
from teinfbot.utils.levels import LevelsUtils
from teinfbot.utils.members import MembersUtils


async def moneyOverTimeStarter(bot: TeinfBot):
    await bot.wait_until_ready()
    moneyOverTime.start(bot)


@tasks.loop(minutes=10)
async def moneyOverTime(bot):
    onlineMembers = MembersUtils.get_online_members(bot)
    onlineMembersIds = [member.id for member in onlineMembers]
    onlineTeinfMembers: List[TeinfMember] = db_session.query(TeinfMember).filter(
        TeinfMember.discordId.in_(onlineMembersIds)).all()
    for onlineTeinfMember in onlineTeinfMembers:
        LEVEL_MULTIPLIER = 1
        level = LevelsUtils.levelFromExp(onlineTeinfMember.exp)
        onlineTeinfMember.money += level * LEVEL_MULTIPLIER
        onlineTeinfMember.exp += level * LEVEL_MULTIPLIER


def setup(bot: TeinfBot):
    bot.loop.create_task(moneyOverTimeStarter(bot))
