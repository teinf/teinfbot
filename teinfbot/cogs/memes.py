import io
import random

import aiohttp
import discord
from bs4 import BeautifulSoup
from discord.ext import commands


class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.memes_channel = self.bot.get_channel(668128841134374924)

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
    async def nowy_mem(self, ctx):
        await ctx.channel.send(embed=await self.get_meme_embed(await self.get_meme(first_page=True)))

    @commands.command()
    async def suchar(self, ctx):
        await ctx.channel.send(await self.get_suchar())


def setup(bot):
    bot.add_cog(Memes(bot))
