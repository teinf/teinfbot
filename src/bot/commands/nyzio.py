import random
import string

import discord
from discord.ext import commands
from discord import app_commands

from bot import Bot


class Nyzio(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    @app_commands.command(name="nyzio", description="Nyzio")
    async def nyzio(self, interaction: discord.Interaction):
        random_letter = random.choice(string.ascii_uppercase)
        await interaction.response.send_message(random_letter + "yzio")

    async def cog_load(self):
        self.bot.tree.add_command(self.nyzio, guild=self.bot.guild)


async def setup(bot: Bot):
    await bot.add_cog(Nyzio(bot))
