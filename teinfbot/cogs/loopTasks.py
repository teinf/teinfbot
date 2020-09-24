import os
import random

from discord.ext import commands, tasks

from teinfbot import TeinfBot
from teinfbot.paths import PATH_ASSETS

class LoopTasks(commands.Cog):

    def __init__(self, bot: TeinfBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.arrow.start()

    @tasks.loop(hours=24)
    async def arrow(self):
        teinf = self.bot.get_guild(self.bot.guild_id)

        ARROW_ID = 239329824361938944
        user = teinf.get_member(ARROW_ID)
        if not user:
            return

        random_przymiotnik = self.random_row_from_file(os.path.join(PATH_ASSETS, 'przymiotniki.txt'))
        random_rzeczownik = self.random_row_from_file(os.path.join(PATH_ASSETS, 'rzeczowniki.txt'))
        random_nickname = random_przymiotnik + " " + random_rzeczownik

        await user.edit(nick=random_nickname)

        channel = teinf.get_channel(720628646267584572)
        await channel.send(f"ARROW: {random_nickname}")

    @staticmethod
    def random_row_from_file(file):
        with open(file, "r") as f:
            if not f.closed:
                return random.choice(f.readlines()).strip()


def setup(bot):
    bot.add_cog(LoopTasks(bot))
