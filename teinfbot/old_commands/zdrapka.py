import random

import discord
from discord.ext import commands

from teinfbot.db import db_session
from teinfbot.models import TeinfMember


@commands.cooldown(3, 60, commands.BucketType.user)
@commands.command()
async def zdrapka(ctx):
    """ KOSZT ZDRAPKI 10 chillcoinów """
    author: TeinfMember = db_session.query(TeinfMember).filter_by(discordId=ctx.author.id).first()

    ZDRAPKA_COST = 5

    if author.money < ZDRAPKA_COST:
        return
    else:
        author.money -= ZDRAPKA_COST

    wygrane = {
        0: 57,
        5: 25,
        10: 10,
        20: 5,
        100: 2,
        500: 1,
    }

    wygrana = random.choices(list(wygrane.keys()), weights=list(wygrane.values()))
    wygrana = wygrana[0]

    if wygrana == 0:
        embed = discord.Embed(title="ZDRAPKA", description=f"{ctx.author} nic nie wygrałeś!",
                              color=discord.Color.red())
    else:
        embed = discord.Embed(title="ZDRAPKA", description=f"{ctx.author} wygrałeś {wygrana} chillcoinów!",
                              color=discord.Color.green())

    author.money += wygrana
    author.exp += wygrana // 5
    embed.set_footer(text=f"Nowy bilans: {author.money}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


@zdrapka.error
async def zdrapka_error(self, ctx, error):
    await ctx.author.send(error)


def setup(bot):
    bot.add_command(zdrapka)
