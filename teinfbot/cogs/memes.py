import io

import aiohttp
from bs4 import BeautifulSoup
from discord.ext import commands

from teinfbot.utils.meme import Meme


class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def get_suchar() -> str:
        my_url = 'http://piszsuchary.pl/losuj'
        async with aiohttp.ClientSession() as session:
            async with session.get(my_url) as resp:
                data = io.BytesIO(await resp.read())
                soup = BeautifulSoup(data, "html.parser")

            match = soup.find("pre", class_="tekst-pokaz")

            return match.text[:-17]

    @commands.command()
    async def mem(self, ctx):
        await ctx.message.delete()
        random_meme = await Meme.random_meme_async()

        await ctx.channel.send(embed=random_meme.embed)

    @commands.command()
    async def suchar(self, ctx):
        await ctx.channel.send(await self.get_suchar())


def setup(bot):
    bot.add_cog(Memes(bot))
