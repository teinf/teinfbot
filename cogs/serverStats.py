import io
import aiohttp
import discord
from discord.ext import commands, tasks
from bs4 import BeautifulSoup


class ServerStats(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @staticmethod
    async def get_trees() -> str:
        my_url = 'https://teamtrees.org'
        async with aiohttp.ClientSession() as session:
            async with session.get(my_url) as resp:
                data = io.BytesIO(await resp.read())
                soup = BeautifulSoup(data, "html.parser")

                match = soup.find('div', class_="counter")
                trees_amount = int(match["data-count"])
                return "{0:,}".format(trees_amount)

    @commands.Cog.listener()
    async def on_ready(self):
        self.treeChannel: discord.TextChannel = self.bot.get_channel(660427011642359811)
        self.refresh_stats.start()

    @tasks.loop(seconds=30.0)
    async def refresh_stats(self):
        await self.treeChannel.edit(name="🌳 " + await self.get_trees())


def setup(bot):
    bot.add_cog(ServerStats(bot))
