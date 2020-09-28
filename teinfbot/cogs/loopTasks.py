import os
import random
from typing import List

import discord
from discord.ext import commands, tasks

from teinfbot import TeinfBot
from teinfbot import db
from teinfbot.models import TeinfMember
from teinfbot.paths import PATH_ASSETS
from teinfbot.db_utils import exp_from_level, level_from_exp

class LoopTasks(commands.Cog):

    def __init__(self, bot: TeinfBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.arrow.start()
        self.money_over_time.start()

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


    @tasks.loop(minutes=10)
    async def money_over_time(self):
        for channel in self.bot.get_all_channels():
            AFK_CHANNEL_ID = 423934688244006913
            members: List[discord.Member] = []
            if str(channel.type) == "voice" and channel.id != AFK_CHANNEL_ID:
                for member in channel.members:
                    members.append(member)

            members_id = [member.id for member in members]
            teinf_members: List[TeinfMember] = db.session.query(TeinfMember).filter(TeinfMember.discordId.in_(members_id)).all()
            for teinf_member in teinf_members:
                LEVEL_MULTIPLIER = 5
                level = level_from_exp(teinf_member.exp)
                teinf_member.money += level * LEVEL_MULTIPLIER
                teinf_member.exp += level * LEVEL_MULTIPLIER


def setup(bot):
    bot.add_cog(LoopTasks(bot))
