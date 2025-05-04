import discord
from discord.ext import commands
from discord import app_commands

from bot import Bot


class Avatar(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @app_commands.command(
        name="avatar",
        description="Wyświetla avatar gracza",
    )
    @app_commands.describe(user="Użytkownik")
    async def avatar(
        self,
        interaction: discord.Interaction,
        user: discord.Member = None,
    ):
        user = user or interaction.user
        await interaction.response.send_message(f"{user.avatar.url}")

    async def cog_load(self):
        self.bot.tree.add_command(self.avatar, guild=self.bot.guild)


async def setup(bot: Bot):
    await bot.add_cog(Avatar(bot))
