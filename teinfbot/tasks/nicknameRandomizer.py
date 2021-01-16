import os
from typing import Tuple

from discord.ext import tasks

from teinfbot.bot import TeinfBot
from teinfbot.paths import ASSETS_PATH
from teinfbot.utils.files import FileUtils


async def randomize_nicknames_starter(bot: TeinfBot):
    await bot.wait_until_ready()
    randomize_nicknames.start(bot)


@tasks.loop(hours=24)
async def randomize_nicknames(bot):
    teinf = bot.get_guild(bot.guild_id)

    RANDOM_NICKNAME_PATH = os.path.join(ASSETS_PATH, "random_nicknames")
    RANDOM_NICKNAME_CHANNEL_ID = 720628646267584572

    randomizeIds: Tuple[int] = (
        239329824361938944,
    )

    for userId in randomizeIds:
        user = teinf.get_member(userId)
        if not user:
            continue

        random_przymiotnik = FileUtils.getRandomLine(os.path.join(RANDOM_NICKNAME_PATH, 'przymiotniki.txt'))
        random_rzeczownik = FileUtils.getRandomLine(os.path.join(RANDOM_NICKNAME_PATH, 'rzeczowniki.txt'))
        random_nickname = random_przymiotnik + " " + random_rzeczownik

        await user.edit(nick=random_nickname)

        channel = teinf.get_channel(RANDOM_NICKNAME_CHANNEL_ID)
        await channel.send(f"ARROW: {random_nickname}")


def setup(bot: TeinfBot):
    bot.loop.create_task(randomize_nicknames_starter(bot))
