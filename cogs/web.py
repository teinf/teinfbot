import io
import aiohttp
import discord
import asyncio
import random
from bs4 import BeautifulSoup
from discord.ext import commands


class Web(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.tree_channel: discord.TextChannel = self.bot.get_channel(660427011642359811)
        self.refresh_stats.start()

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

    @tasks.loop(seconds=30.0)
    async def refresh_stats(self):
        await self.tree_channel.edit(name="🌳 " + await self.get_trees())

    @staticmethod
    async def get_suchar() -> str:
        my_url = 'http://piszsuchary.pl/losuj'
        async with aiohttp.ClientSession() as session:
            async with session.get(my_url) as resp:
                data = io.BytesIO(await resp.read())
                soup = BeautifulSoup(data, "html.parser")

            match = soup.find("pre", class_="tekst-pokaz")

            return match.text[:-17]

    @staticmethod
    async def get_meme(full_page=False, first_page=False):
        """ ZWRACA (url, tytul)"""
        my_url = 'https://jbzd.com.pl/str/'
        if not first_page:
            my_url += str(random.randint(1, 150))
        else:
            my_url += "1"

        async with aiohttp.ClientSession() as session:
            async with session.get(my_url) as resp:
                data = io.BytesIO(await resp.read())
                soup = BeautifulSoup(data, "html.parser")

                images = soup.find_all("img", class_="article-image")
                images_url = [(image['src'], image['alt']) for image in images]

        if not full_page:
            return random.choice(images_url)
        else:
            return images_url

    @staticmethod
    async def get_meme_embed(meme) -> discord.Embed:
        em = discord.Embed(
            title=meme[1],
        )

        em.set_image(url=meme[0])

        return em

    @commands.command()
    async def mem(self, ctx):
        await ctx.channel.send(embed=await self.get_meme_embed(await self.get_meme()))

    @commands.command()
    async def strona_memow(self, ctx):
        for meme in await self.get_meme(full_page=True):
            await ctx.channel.send(embed=await self.get_meme_embed(meme))

    @commands.command()
    async def nowy_mem(self, ctx):
        await ctx.channel.send(embed=await self.get_meme_embed(await self.get_meme(first_page=True)))

    @commands.command()
    async def suchar(self, ctx):
        await ctx.channel.send(await self.get_suchar())
