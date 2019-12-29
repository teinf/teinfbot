import discord,asyncio, random
from discord.ext import commands

class Moderacja(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def clear(self, ctx, amount: int = 5):
        await ctx.channel.purge(limit=amount)

    @commands.command()
    async def cleanbot(self, ctx):
        def check(msg):
            return msg.author.name == "TEINF"
        await ctx.channel.purge(limit = 15, check=check)


def setup(bot):
    bot.add_cog(Moderacja(bot))
