import random

import discord
from discord.ext import commands
from discord import app_commands

from bot import Bot


class Kutas(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    @app_commands.command(
        name="kutas",
        description="Sprawdź rozmiar swojej knagi",
    )
    async def kutas(self, interaction: discord.Interaction):
        kutas_len = random.randint(0, 30)

        if kutas_len == 0:
            em = discord.Embed(
                title="Przypał",
                description=f"{interaction.user.mention} nie masz chuja xd",
                colour=discord.Color.red(),
            )
        elif kutas_len < 10:
            em = discord.Embed(
                title="YELLOW DIK",
                description=f"{interaction.user.mention} twój mały ma {kutas_len} cm! Współczuję Ci :(",
                colour=discord.Color.gold(),
            )
        elif 10 <= kutas_len < 20:
            em = discord.Embed(
                title="WHITE DIK",
                description=f"{interaction.user.mention} twój normalny ma {kutas_len} cm! Nadal za mały ale ok",
                colour=discord.Color.from_rgb(255, 255, 255),
            )
        else:
            em = discord.Embed(
                title="BLAKK DIK",
                description=f"{interaction.user.mention} twoje monstrum ma {kutas_len} cm!",
                colour=discord.Color.from_rgb(0, 0, 0),
            )

        await interaction.response.send_message(embed=em)

    async def cog_load(self):
        self.bot.tree.add_command(self.kutas, guild=self.bot.guild)


async def setup(bot: Bot):
    await bot.add_cog(Kutas(bot))
