import random

import discord
from discord.ext import commands
from discord_slash import SlashContext, cog_ext

from teinfbot.bot import TeinfBot
from teinfbot.utils.guilds import guild_ids


class Kutas(commands.Cog):
    def __init__(self, bot: TeinfBot):
        self.bot: TeinfBot = bot

    @cog_ext.cog_slash(name="kutas", description="B======D", guild_ids=guild_ids)
    async def __kutas(self, ctx: SlashContext):
        await ctx.ack(True)

        kutas_len = random.randint(0, 30)
        if kutas_len == 0:
            em = discord.Embed(
                title="Przypał",
                description=f"{ctx.author.mention} nie masz chuja xd",
                colour=discord.Color.red()
            )
        if kutas_len < 10:
            em = discord.Embed(
                title="YELLOW DIK",
                description=f"{ctx.author.mention} twój mały ma {kutas_len} cm! Współczuję Ci :(",
                colour=discord.Color.gold()
            )
        elif 10 <= kutas_len < 20:
            em = discord.Embed(
                title="WHITE DIK",
                description=f"{ctx.author.mention} twój normalny ma {kutas_len} cm! Nadal za mały ale ok",
                colour=discord.Color.from_rgb(255, 255, 255)
            )
        else:
            em = discord.Embed(
                title="BLAKK DIK",
                description=f"{ctx.author.mention} twoje monstrum ma {kutas_len} cm!",
                colour=discord.Color.from_rgb(0, 0, 0)
            )

        await ctx.send(embed=em)


def setup(bot: TeinfBot):
    bot.add_cog(Kutas(bot))
