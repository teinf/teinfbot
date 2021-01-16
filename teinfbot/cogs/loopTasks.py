import os
import random
from typing import List

import discord
from discord.ext import commands, tasks

from teinfbot import TeinfBot
from teinfbot import db_session
from teinfbot.db_utils import level_from_exp
from teinfbot.models import TeinfMember
from teinfbot.paths import PATH_ASSETS


class LoopTasks(commands.Cog):

    def __init__(self, bot: TeinfBot):
        self.bot = bot
        self.startTasks = False

    @commands.Cog.listener()
    async def on_ready(self):
        self.arrow.start()
        self.money_over_time.start()
        self.addTimeSpent.start()
        self.startTasks = True

    @tasks.loop(hours=24)
    async def arrow(self):
        teinf = self.bot.get_guild(self.bot.guild_id)
        ARROW_ID = 239329824361938944
        user = teinf.get_member(ARROW_ID)
        if not user:
            return

        RANDOM_NICKNAME_PATH = os.path.join(PATH_ASSETS, "random_nicknames")
        random_przymiotnik = self.random_row_from_file(os.path.join(RANDOM_NICKNAME_PATH, 'przymiotniki.txt'))
        random_rzeczownik = self.random_row_from_file(os.path.join(RANDOM_NICKNAME_PATH, 'rzeczowniki.txt'))
        random_nickname = random_przymiotnik + " " + random_rzeczownik

        await user.edit(nick=random_nickname)

        channel = teinf.get_channel(720628646267584572)
        await channel.send(f"ARROW: {random_nickname}")

    @staticmethod
    def random_row_from_file(file):
        with open(file, "r") as f:
            if not f.closed:
                return random.choice(f.readlines()).strip()

    def get_online_members(self) -> List[discord.Member]:
        members: List[discord.Member] = []
        for channel in self.bot.get_all_channels():
            AFK_CHANNEL_ID = 423934688244006913
            if str(channel.type) == "voice" and channel.id != AFK_CHANNEL_ID:
                for member in channel.members:
                    members.append(member)
        return members

    @tasks.loop(minutes=10)
    async def money_over_time(self):
        if not self.startTasks:
            return
        onlineMembers = self.get_online_members()
        onlineMembersIds = [member.id for member in onlineMembers]
        onlineTeinfMembers: List[TeinfMember] = db_session.query(TeinfMember).filter(
            TeinfMember.discordId.in_(onlineMembersIds)).all()
        for onlineTeinfMember in onlineTeinfMembers:
            LEVEL_MULTIPLIER = 1
            level = level_from_exp(onlineTeinfMember.exp)
            onlineTeinfMember.money += level * LEVEL_MULTIPLIER
            onlineTeinfMember.exp += level * LEVEL_MULTIPLIER

    @tasks.loop(minutes=1)
    async def addTimeSpent(self):
        onlineMembers = self.get_online_members()
        onlineMembersIds = [member.id for member in onlineMembers]
        onlineTeinfMembers: List[TeinfMember] = db_session.query(TeinfMember).filter(
            TeinfMember.discordId.in_(onlineMembersIds)).all()

        for onlineTeinfMember in onlineTeinfMembers:
            onlineTeinfMember.timespent += 1


def setup(bot):
    bot.add_cog(LoopTasks(bot))
