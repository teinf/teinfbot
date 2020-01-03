import discord
from discord.ext import commands
import random


class Nazwa(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="joink")
    async def joink(self, ctx):
        await ctx.channel.send("joink :D")

    @commands.command(name="kamin")
    async def kamin(self, ctx: commands.Context, *cos):
        if cos == tuple():
            msg_em = discord.Embed(
                title="PKN",
                description="Cłopie wybierz coś!",
                colour=discord.Color.magenta()
            )
            await ctx.channel.send(embed=msg_em)
            return

        lista = ["p", "k", "n"]
        user_choice = cos[0][0].lower()
        c_choice = random.choice(lista)
        both_choices = user_choice+c_choice

        if c_choice == user_choice:
            msg_em = discord.Embed(
                title="PKN",
                description="Draw " + ctx.author.name,
                colour=discord.Color.orange()
            )
        elif both_choices in ["pn", "kp", "nk"]:
            msg_em = discord.Embed(
                title="PKN",
                description="You LOSE " + ctx.author.name,
                colour=discord.Color.dark_red()
            )
        else:
            msg_em = discord.Embed(
                title="PKN",
                description="You WIN " + ctx.author.name,
                colour=discord.Color.gold()
            )
        await ctx.channel.send(embed=msg_em, delete_after=30)
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(Nazwa(bot))
