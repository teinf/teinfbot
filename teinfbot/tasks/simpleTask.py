from discord.ext import tasks

from teinfbot.bot import TeinfBot


async def taskStarter(bot: TeinfBot):
    await bot.wait_until_ready()
    task.start(bot)


@tasks.loop(seconds=1)
async def task(bot: TeinfBot):
    print(bot.user.mention)


def setup(bot: TeinfBot):
    return
    bot.loop.create_task(taskStarter(bot))
