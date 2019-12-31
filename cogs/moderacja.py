import discord, asyncio, random
from discord.ext import commands


class Moderacja(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role("🛠  MODERATOR  🛠")
    async def clear(self, ctx, amount: int = 5):
        if amount > 50:
            amount=50
        await ctx.channel.purge(limit=amount)


def setup(bot):
    bot.add_cog(Moderacja(bot))
