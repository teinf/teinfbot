import random

import discord
from discord.ext import commands


class Randomizer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="lt")
    @commands.cooldown(1, 60, commands.BucketType.default)
    async def losowanie_teamu(self, ctx, num_of_teams: int = 2):
        """LOSUJE TEAM !"""

        author = ctx.message.author  # osoba która wywołała komende
        await ctx.message.delete()  # usunięcie wiadomosci '.losowanie_teamu'

        em = discord.Embed(
            title=":star2: LOSOWANIE TEAMU :star2:",
            description="ABY **DOŁĄCZYĆ** :white_check_mark:\n**KONIEC** CZEKANIA :x:",
            colour=discord.Colour.gold()
        )
        # wysyłanie wiadomości i zapisywanie jej do message
        message = await ctx.send(embed=em)

        emoji_check = '\u2705'
        emoji_cross = '\u274C'

        await message.add_reaction(emoji_check)
        await message.add_reaction(emoji_cross)

        def check(r, user):
            # czekanie na dodawanie reakcji ❌ przez tego kto wywołał komende
            return str(r.emoji) == emoji_cross and user.id == author.id

        # czekanie na dodanie reakcji ❌
        await self.bot.wait_for('reaction_add', timeout=60.0, check=check)

        # musimy odświeżyć informacje o dodanych reakcjach
        message = await ctx.fetch_message(message.id)

        reaction = message.reactions[0]  # wzięcie 1 reakcji w tym przypadku ✅

        # ZAMIANIA reaction.users(): AsyncIterator na reaction.users(): list poprzez flatten()
        users = await reaction.users().flatten()
        patricipants = [user.id for user in users if user.name != "TEINF"]
        random.shuffle(patricipants)  # mieszanie listy

        teams = []
        for i in range(1, num_of_teams + 1):
            teams.append(patricipants[i - 1::num_of_teams])

        message = await ctx.fetch_message(message.id)
        await message.delete()  # usuwanie wcześniej wysłanych wiadomości

        for i, team in enumerate(teams):
            color = discord.Colour.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            teamStr = ""
            for userNumber, userId in enumerate(team, start=1):
                teamStr += f"{userNumber}. <@{userId}>\n"

            team_embed = discord.Embed(
                title=f"TEAM {i + 1}", description=teamStr, colour=color)

            await ctx.send(embed=team_embed)

    @commands.command()
    async def kostka(self, ctx: commands.Context):
        await ctx.channel.send(random.randint(1, 6))

    @commands.command()
    async def moneta(self, ctx: commands.Context):
        randomNumber = random.randint(1, 2)
        throwResult = "ORZEŁ" if randomNumber == 1 else "RESZKA"
        await ctx.channel.send(throwResult)

    @commands.command()
    async def losowaLiczba(self, ctx: commands.Context, minBound: int, maxBound: int):
        await ctx.channel.send(random.randint(minBound, maxBound))


def setup(bot):
    bot.add_cog(Randomizer(bot))
