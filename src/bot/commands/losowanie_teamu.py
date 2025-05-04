import random
from typing import List

import discord
from discord.ext import commands
from discord import app_commands

from bot import Bot


class JoinView(discord.ui.View):
    def __init__(self, author: discord.User, timeout: float = 300):
        super().__init__(timeout=timeout)
        self.users = []
        self.author = author
        self.finished = False

    @discord.ui.button(label="Dołącz", style=discord.ButtonStyle.green, emoji="✅")
    async def join(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user not in self.users:
            self.users.append(interaction.user)
        await self.update_embed(interaction)

    @discord.ui.button(label="Wyjdź", style=discord.ButtonStyle.danger, emoji="⛔")
    async def leave(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user in self.users:
            self.users.remove(interaction.user)
        await self.update_embed(interaction)

    @discord.ui.button(label="Losuj", style=discord.ButtonStyle.grey, emoji="🎲")
    async def end(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.author.id:
            await interaction.response.send_message(
                "Tylko autor komendy może zakończyć losowanie.", ephemeral=True
            )
            return
        self.finished = True
        self.stop()
        await interaction.response.defer()

    async def update_embed(self, interaction: discord.Interaction):
        description = (
            "Gracze: " + ", ".join(user.mention for user in self.users)
            if self.users
            else "Brak graczy."
        )
        embed = discord.Embed(
            title=":star2: LOSOWANIE TEAMU :star2:",
            description=description,
            colour=discord.Colour.gold(),
        )
        await interaction.response.edit_message(embed=embed, view=self)


class LosowanieTeamu(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    @app_commands.command(name="lt", description="Wylosowanie teamów")
    @app_commands.describe(ilosc_druzyn="Ilość drużyn do losowania teamu")
    async def lt(self, interaction: discord.Interaction, ilosc_druzyn: int):
        view = JoinView(author=interaction.user)

        embed = discord.Embed(
            title=":star2: LOSOWANIE TEAMU :star2:",
            description="ABY **DOŁĄCZYĆ** :white_check_mark:\n**KONIEC** CZEKANIA :x:",
            colour=discord.Colour.gold(),
        )

        message = await interaction.response.send_message(embed=embed, view=view)
        await view.wait()

        await interaction.delete_original_response()  # remove the interactive message

        # Shuffle and split into teams
        users = view.users
        random.shuffle(users)
        teams: List[List[discord.User]] = []

        for i in range(ilosc_druzyn):
            teams.append(users[i::ilosc_druzyn])

        # Send result
        for i, team in enumerate(teams):
            members_text = "\n".join(
                f"{j + 1}. {user.mention}" for j, user in enumerate(team)
            )
            team_embed = discord.Embed(
                title=f"TEAM {i + 1}",
                description=members_text or "Brak graczy.",
                colour=discord.Color.random(),
            )
            await interaction.channel.send(embed=team_embed)

    async def cog_load(self):
        self.bot.tree.add_command(self.lt, guild=self.bot.guild)


async def setup(bot: Bot):
    await bot.add_cog(LosowanieTeamu(bot))
