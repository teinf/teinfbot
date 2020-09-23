import discord
import random
from discord.ext import commands
import os

class Zabawa(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="kutas")
    async def kutas(self, ctx):
        kutas_len = random.randint(1, 30)
        if kutas_len < 10:
            em = discord.Embed(
                title="YELLO DIK",
                description=f"{ctx.author.name} twój mały ma {kutas_len} cm! Współczuję Ci :(",
                colour=discord.Color.gold()
            )
        elif 10 <= kutas_len < 20:
            em = discord.Embed(
                title="WHITE DIK",
                description=f"{ctx.author.name} twój normalny ma {kutas_len} cm! Nadal za mały ale ok",
                colour=discord.Color.from_rgb(255, 255, 255)
            )
        else:
            em = discord.Embed(
                title="BLAKK DIK",
                description=f"{ctx.author.name} twój BBC ma {kutas_len} cm! Witamy in WAKANDA",
                colour=discord.Color.from_rgb(0, 0, 0)
            )

        await ctx.send(embed=em)
        await ctx.message.delete()

    @commands.command()
    async def nyzio(self, ctx):
        alphabet = "ABCDEFGHIJKLMNOPRSTUVWXYZ"
        random_letter = random.choice(alphabet)
        await ctx.send(random_letter + "yzio")
    


def setup(bot):
    bot.add_cog(Zabawa(bot))
