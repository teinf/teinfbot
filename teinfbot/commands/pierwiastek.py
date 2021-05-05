from discord.ext import commands
from discord.ext import commands
from discord_slash import SlashContext, SlashCommandOptionType, cog_ext
from discord_slash.utils import manage_commands

from teinfbot.bot import TeinfBot
from teinfbot.utils.guilds import guild_ids


class Pierwiastek(commands.Cog):
    def __init__(self, bot: TeinfBot):
        self.bot: TeinfBot = bot

    def rozklad(self, n):

        if n > 10e06:
            return "0"

        dzielniki = {}

        while n > 1:
            for i in range(2, n + 1):
                if n % i == 0:
                    n //= i
                    if dzielniki.get(i):
                        dzielniki[i] += 1
                    else:
                        dzielniki[i] = 1

                    break

        lewaStrona = 1
        prawaStrona = 1

        for dzielnik in dzielniki:
            lewaStrona *= (dzielnik ** (dzielniki[dzielnik] // 2))
            prawaStrona *= (dzielnik ** (dzielniki[dzielnik] % 2))

        znakPierwiastka = u"\u221a"
        if lewaStrona == 1:
            return znakPierwiastka + str(prawaStrona)
        elif prawaStrona == 1:
            return str(lewaStrona)
        else:
            return str(lewaStrona) + znakPierwiastka + str(prawaStrona)

    @cog_ext.cog_slash(name="pierwiastek", guild_ids=guild_ids, description="Pierwiastkuje liczbę", options=[
        manage_commands.create_option(
            name="liczba",
            description="Liczba do spierwiastkowania",
            option_type=SlashCommandOptionType.INTEGER,
            required=True
        )
    ])
    async def __pierwiastek(self, ctx: SlashContext, liczba: int):
        
        await ctx.send(f"{liczba}: {self.rozklad(liczba)}")


def setup(bot: TeinfBot):
    bot.add_cog(Pierwiastek(bot))
