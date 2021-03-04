import random

import discord
from discord.ext import commands
from discord_slash import SlashContext, SlashCommandOptionType, cog_ext
from discord_slash.utils import manage_commands

from teinfbot.bot import TeinfBot
from teinfbot.utils.guilds import guild_ids


class Lt(commands.Cog):
    def __init__(self, bot: TeinfBot):
        self.bot: TeinfBot = bot

    @cog_ext.cog_slash(name="lt", guild_ids=guild_ids, description="Wylosowanie teamów", options=[
        manage_commands.create_option(
            name="ilosc_druzyn",
            description="Ilość drużyn do losowania teamu",
            option_type=SlashCommandOptionType.INTEGER,
            required=True
        )
    ])
    async def __lt(self, ctx: SlashContext, ilosc_druzyn: int):
        await ctx.ack(True)

        author = ctx.author  # osoba która wywołała komende

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
        await ctx.bot.wait_for('reaction_add', timeout=60.0, check=check)

        # musimy odświeżyć informacje o dodanych reakcjach
        message = await ctx.channel.fetch_message(message.id)

        reaction = message.reactions[0]  # wzięcie 1 reakcji w tym przypadku ✅

        # ZAMIANIA reaction.users(): AsyncIterator na reaction.users(): list poprzez flatten()
        users = await reaction.users().flatten()
        users = [user for user in users if not user.bot]

        random.shuffle(users)

        teams: List[discord.User] = []
        for i in range(1, ilosc_druzyn + 1):
            teams.append(users[i - 1::ilosc_druzyn])

        message = await ctx.channel.fetch_message(message.id)
        await message.delete()  # usuwanie wcześniej wysłanych wiadomości

        for i, team in enumerate(teams):
            color = discord.Color.random()

            team_users = ""
            for userNumber, user in enumerate(team, start=1):
                team_users += f"{userNumber}. {user.mention}\n"

            team_embed = discord.Embed(title=f"TEAM {i + 1}", description=team_users, colour=color)

            await ctx.send(embed=team_embed)


def setup(bot: TeinfBot):
    bot.add_cog(Lt(bot))
