import os
from typing import Tuple

from discord.ext import commands, tasks

from teinfbot import TeinfBot
from teinfbot.paths import PATH_ASSETS
from teinfbot.utils.files import FileUtils


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

        RANDOM_NICKNAME_PATH = os.path.join(PATH_ASSETS, "random_nicknames")
        RANDOM_NICKNAME_CHANNEL_ID = 720628646267584572

        for userId in self.randomizeIds:
            user = teinf.get_member(userId)
            if not user:
                continue

            random_przymiotnik = FileUtils.getRandomLine(os.path.join(RANDOM_NICKNAME_PATH, 'przymiotniki.txt'))
            random_rzeczownik = FileUtils.getRandomLine(os.path.join(RANDOM_NICKNAME_PATH, 'rzeczowniki.txt'))
            random_nickname = random_przymiotnik + " " + random_rzeczownik

            await user.edit(nick=random_nickname)

            channel = teinf.get_channel(RANDOM_NICKNAME_CHANNEL_ID)
            await channel.send(f"ARROW: {random_nickname}")
