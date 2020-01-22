import discord, random
from discord.ext import commands
import utils


class Kasyno(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ruletka_help(self, ctx):
        em = discord.Embed(title="\U0001F4B0 Ruletka", description="", color=discord.Colour.gold())
        em.add_field(name="Bety", value="**<czarny, czerwony, zielony>** lub **<b, r, g>**", inline=False)
        em.add_field(name="Info",
                     value="**Czarny/Czerwony/Zielony** - jeżeli bot wyrzuci Twój **kolor**, wygrywasz\n**0-36** - jeżeli bot wyrzuci Twój **numer**, wygrywasz\n**Niskie/Wysokie** - **niskie** = 1-18, **wysokie** = 19-36\n**Nieparzyste/Parzyste** - **nieparzyste** = 1, 3, 5, ..., 35, **parzyste** = 2, 4, 6, ..., 36",
                     inline=False)
        em.add_field(name="Wygrane",
                     value="1.**Czarny/Czerwony** - 2x\n2.**0-36** lub **Zielony** - 35x\n3.**wysoki/niski** - 2x\n4.**parzysty/nieparzysty** - 2x",
                     inline=False)
        em.add_field(name="Numery",
                     value=":green_heart: Zielony: **0**\n:black_heart: Czarne: **2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35**\n:heart: Czerwone: **1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36**",
                     inline=True)
        em.add_field(name="Użycie", value=".ruletka **<bet>**")
        await ctx.send(embed=em)

    @commands.command()
    async def ruletka(self, ctx, typ: str, bet: int):
        czarne = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
        czerwone = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]

        if bet <= 0:
            return

        # await utils.add_digits(message, 4)
        # reaction, user = await self.bot.wait_for(
        #     "reaction_add",
        #     check=lambda react, usr: react.message == ctx.message and usr == ctx.author)
        #
        # result = utils.get_emoji_value(reaction.emoji)

        winning_number = random.randint(0, 36)

        desc = ""
        if winning_number in czarne:
            desc += "Czarna\n"
        elif winning_number in czerwone:
            desc += "Czerwona\n"
        elif winning_number == 0:
            desc += "Zielona"
        if winning_number % 2 == 0:
            desc += "Parzysta"
        else:
            desc += "Nieparzysta"

        red_names = ['r', 'red', 'czerwone', 'czerwony', "czerwona"]
        black_names = ["b", 'black', 'czarne', 'czarny', "czarna"]
        green_names = ['g', 'green', 'zielone', 'zielony']

        parzyste_names = ["parzyste", "p", "parzysta"]
        nieparzyste_names = ["nieparzyste", 'n', 'nieparzysta']

        high_names = ["high", "wysokie", "wysoki"]
        low_names = ["low", "niskie", "niski"]

        wygrana = 0

        try:
            if int(typ) == winning_number:
                wygrana = bet * 35
        except ValueError as e:
            pass

        if typ in red_names + black_names + green_names:
            print("RED", "BLACK", "GREEN")
            if typ in red_names:
                if winning_number in czerwone:
                    wygrana = bet * 2
            elif typ in black_names:
                if winning_number in czarne:
                    wygrana = bet * 2
            elif typ in green_names:
                if winning_number == 0:
                    wygrana = bet * 35

        elif typ in parzyste_names + nieparzyste_names:
            print("PARZYSTA", "NIEPARZYSTA", winning_number % 2)
            if winning_number % 2 == 0 and typ in parzyste_names:
                print("PARZYSTA")
                wygrana = bet * 2
            elif winning_number % 2 == 1 and typ in nieparzyste_names:
                print("NIEPARZYSTA")
                wygrana = bet * 2
            else:
                print("PRZEGRANA")
                wygrana = 0

        elif typ in high_names + low_names:
            print("HIGH", "LOW")
            if winning_number >= 19 and typ in high_names:
                wygrana = bet * 2
            elif winning_number < 19 and typ in low_names:
                wygrana = bet * 2
            else:
                wygrana = 0

        if wygrana <= 0:
            kolor = discord.Color.red()
            text = "PRZEGRAŁEŚ! \U0001F602"
        else:
            kolor = discord.Color.green()
            text = "WYGRAŁEŚ!"

        em = discord.Embed(title=f"\U0001F4B0 Ruletka: {ctx.message.author} \U0001F4B0", colour=kolor)
        em.add_field(name=f"**{text}**", value=f"Wygrywająca liczba : **{winning_number}**", inline=False)
        em.add_field(name=f"**INFO O LICZBIE**", value=desc)
        if wygrana > 0:
            em.add_field(name="**Profit** :", value=f"**+{wygrana}** chillcoinsów", inline=False)
        em.set_footer(text=str(ctx.author) + f": +{wygrana}CC, +{wygrana // 10}EXP", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Kasyno(bot))
