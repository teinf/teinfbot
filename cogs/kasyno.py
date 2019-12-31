import discord, random
from discord.ext import commands


class Kasyno(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def ruletka(self, ctx, *args):
        czarne = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
        czerwone = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]

        try:
            typ = str(args[0])
            bet = float(args[1])
        except:
            em = discord.Embed(title="\U0001F4B0 Ruletka", description="", color=discord.Colour.gold())
            em.add_field(name="Bety", value="**<czarny, czerwony, zielony>** lub **<b, r, g>**", inline=False)
            em.add_field(name="Info",
                         value="**Czarny/Czerwony/Zielony** - jeżeli bot wyrzuci Twój **kolor**, wygrywasz\n**0-36** - jeżeli bot wyrzuci Twój **numer**, wygrywasz\n**Niskie/Wysokie** - **niskie** = 1-18, **wysokie** = 19-36\n**Nieparzyste/Parzyste** - **nieparzyste** = 1, 3, 5, ..., 35, **parzyste** = 2, 4, 6, ..., 36",
                         inline=False)
            em.add_field(name="Wygrane",
                         value="**Czarny/Czerwony** - 2x\n**0-36** lub **Zielony** - 35x\n**wysoki/niski** - 2x\n**parzysty/nieparzysty** - 2x",
                         inline=False)
            em.add_field(name="Numery",
                         value=":green_heart: Zielony: **0**\n:black_heart: Czarne: **2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35**\n:heart: Czerwone: **1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36**",
                         inline=True)
            em.add_field(name="Użycie", value=".ruletka **<typ beta> <bet>**")
            await ctx.send(embed=em)
        else:
            losowa_liczba = random.choice(range(37))

            if losowa_liczba in czarne:
                kolor = discord.Colour.from_rgb(0, 0, 0)
            elif losowa_liczba in czerwone:
                kolor = discord.Colour.red()
            else:
                kolor = discord.Colour.green()

            wygrana = None
            if typ in ['r', 'red', 'czerwone', 'czerwony']:
                if losowa_liczba in czerwone:
                    wygrana = bet * 2
            elif typ in ["b", 'black', 'czarne', 'czarny']:
                if losowa_liczba in czarne:
                    wygrana = bet * 2
            elif typ in ['g', 'green', 'zielone', 'zielony']:
                if losowa_liczba == 0:
                    wygrana = bet * 35

            if wygrana is None:
                text = "PRZEGRAŁEŚ! \U0001F602"
                znak = "-"
            else:
                text = "WYGRAŁEŚ!"
                znak = "+"

            em = discord.Embed(title=f"\U0001F4B0 Ruletka: {ctx.message.author}", description="", colour=kolor)
            em.add_field(name=f"**{text}**", value=f"Wygrywająca liczba : **{losowa_liczba}**", inline=False)
            em.add_field(name="Profit :", value=f"**{znak}{bet}** \U0001F4C0 płytkje", inline=False)

            await ctx.send(embed=em, delete_after=60)


def setup(bot):
    bot.add_cog(Kasyno(bot))
