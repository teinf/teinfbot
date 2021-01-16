from discord.ext import commands
import random
import string


@commands.command()
async def nyzio(ctx: commands.Context):
    random_letter = random.choice(string.ascii_uppercase)
    await ctx.send(random_letter + "yzio")


def setup(bot):
    bot.add_command(nyzio)
