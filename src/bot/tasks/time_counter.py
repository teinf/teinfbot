from discord.ext import tasks, commands

from bot import Bot
from db.models import User


class TimeCounter(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.time_counter.start()

    def cog_unload(self):
        self.time_counter.cancel()

    @tasks.loop(minutes=1)
    async def time_counter(self):
        await self.bot.wait_until_ready()
        online_members = await self.bot.get_members_in_voice_channels()
        ids = [m.id for m in online_members]
        print(f"Time update for {ids}")
        await User.increment_time(ids, 1)

    @time_counter.before_loop
    async def before_time_counter(self):
        await self.bot.wait_until_ready()


async def setup(bot: Bot):
    await bot.add_cog(TimeCounter(bot))
