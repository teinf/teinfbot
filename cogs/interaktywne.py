import discord
import asyncio
import random
from discord.ext import commands


class Interaktywne(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, name="losowanie_teamu", aliases=["team_losowanie", "team_l", "losowanie_t", "lt"])
    @commands.cooldown(1, 60, commands.BucketType.default)
    async def losowanie_teamu(self, ctx, numberOfTeams: int = 2):
        """LOSUJE TEAM !"""

        author = ctx.message.author  # osoba która wywołała komende
        await ctx.message.delete()  # usunięcie wiadomosci '.losowanie_teamu'

        em = discord.Embed(title=":star2: LOSOWANIE TEAMU :star2:",
                           description="ABY **DOŁĄCZYĆ** :white_check_mark:\n**KONIEC** CZEKANIA :x:", colour=discord.Colour.gold())
        # wysyłanie wiadomości i zapisywanie jej do message
        message = await ctx.send(embed=em)

        await message.add_reaction("\u2705")  # dodawanie reakcji ✅
        await message.add_reaction("\u274C")  # dodawanie reakcji ❌

        def check(reaction, user):
            # czekanie na dodawanie reakcji ❌ przez tego kto wywołał komende
            return str(reaction.emoji) == "\u274C" and user.id == author.id

        # czekanie na dodanie reakcji ❌
        await self.bot.wait_for('reaction_add', timeout=60.0, check=check)

        # musimy odświeżyć informacje o dodanych reakcjach
        message = await ctx.get_message(message.id)

        reaction = message.reactions[0]  # wzięcie 1 reakcji w tym przypadku ✅

        # ZAMIANIA reaction.users(): AsyncIterator na reaction.users(): list poprzez flatten()
        users = await reaction.users().flatten()

        uczestnicy = [user.name for user in users]
        uczestnicy.remove("TEINF")
        random.shuffle(uczestnicy)  # mieszanie listy

        teams = []
        for i in range(1, numberOfTeams+1):
            teams.append(uczestnicy[i-1::numberOfTeams])

        message = await ctx.get_message(message.id)
        await message.delete()  # usuwanie wcześniej wysłanych wiadomości

        colors = [discord.Colour.blue, discord.Colour.red, discord.Colour.green,
                  discord.Colour.orange, discord.Colour.purple, discord.Colour.gold]
        circles = [':large_blue_circle:', ':red_circle:',
                   ':black_circle:', ':white_circle:']
        for i, team in enumerate(teams):
            color = random.choice(colors)
            teamStr = ", ".join(team)
            circle = random.choice(circles)
            team_embed = discord.Embed(
                title=f"{circle} TEAM {i+1} {circle}", description=teamStr, colour=color())
            await ctx.send(embed=team_embed, delete_after=120)


def setup(bot):
    bot.add_cog(Interaktywne(bot))
