from typing import List

from discord.ext import commands, tasks

from teinfbot import TeinfBot
from teinfbot import db_session
from teinfbot.models import TeinfMember
from teinfbot.utils.levels import LevelsUtils
from teinfbot.utils.members import MembersUtils


class LoopTasks(commands.Cog):

    def __init__(self, bot: TeinfBot):
        self.bot = bot
        self.startTasks = False

    @commands.Cog.listener()
    async def on_ready(self):
        self.money_over_time.start()
        self.addTimeSpent.start()
        self.startTasks = True

    @tasks.loop(minutes=10)
    async def money_over_time(self):
        if not self.startTasks:
            return
        onlineMembers = MembersUtils.get_online_members(self.bot)
        onlineMembersIds = [member.id for member in onlineMembers]
        onlineTeinfMembers: List[TeinfMember] = db_session.query(TeinfMember).filter(
            TeinfMember.discordId.in_(onlineMembersIds)).all()
        for onlineTeinfMember in onlineTeinfMembers:
            LEVEL_MULTIPLIER = 1
            level = LevelsUtils.levelFromExp(onlineTeinfMember.exp)
            onlineTeinfMember.money += level * LEVEL_MULTIPLIER
            onlineTeinfMember.exp += level * LEVEL_MULTIPLIER

    @tasks.loop(minutes=1)
    async def addTimeSpent(self):
        onlineMembers = MembersUtils.get_online_members(self.bot)
        onlineMembersIds = [member.id for member in onlineMembers]
        onlineTeinfMembers: List[TeinfMember] = db_session.query(TeinfMember).filter(
            TeinfMember.discordId.in_(onlineMembersIds)).all()

        for onlineTeinfMember in onlineTeinfMembers:
            onlineTeinfMember.timespent += 1


def setup(bot):
    bot.add_cog(LoopTasks(bot))
