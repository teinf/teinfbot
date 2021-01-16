from teinfbot import TeinfBot
import discord
from discord.ext import commands, tasks
from typing import Tuple
from teinfbot.paths import PATH_ASSETS
import os

class RandomNickname(commands.Cog):
    def __init__(self, bot: TeinfBot):
        self.bot = bot
        self.randomizeIds: Tuple[int] = (
            239329824361938944,
        )

    @commands.Cog.listener()
    async def on_ready(self):
        self.randomize_nicknames.start()

    @tasks.loop(hours=24)
    async def randomize_nicknames(self):
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