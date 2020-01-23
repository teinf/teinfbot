import discord, random
from discord.ext import commands
import utils
from waluta import Baza


class Kasyno(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ruletka_help(self, ctx):
        em = discord.Embed(title="\U0001F4B0 Ruletka", description="", color=discord.Colour.gold())
        em.add_field(name="Bety", value="**<czarny, czerwony, zielony>** lub **<b, r, g>**", inline=False)
        em.add_field(name="Info",
                     value="**Czarny/Czerwony/Zielony** - jeżeli bot wyrzuci Twój **kolor**, wygrywasz",
                     inline=False)
        em.add_field(name="Wygrane",
                     value="1.**Czarny/Czerwony** - 2x\n**Zielony** - 35x",
                     inline=False)
        em.add_field(name="Numery",
                     value=":green_heart: Zielony: **0**\n:black_heart: Czarne: **2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35**\n:heart: Czerwone: **1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36**",
                     inline=True)
        em.add_field(name="Użycie", value=".ruletka **<bet>**")
        await ctx.send(embed=em)

    @commands.command()
    async def ruletka(self, ctx, bet: int):

        if bet <= 0:
            return

        money = Baza.get_money(ctx.author.id)
        if money < bet:
            await ctx.author.send(f"Nie masz wystarczająco pieniędzy - brakuje `{abs(bet - money)}` chillcoinów")
            return

        Baza.add_money(ctx.author.id, -bet)

        czarne = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
        czerwone = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]

        embed = discord.Embed(
            title=f"🎰 Ruletka 🎰",
            description=f"Wybierz kolor:",
            color=discord.Color.gold()
        )

        embed.set_footer(text=f"{str(ctx.author)}", icon_url=ctx.author.avatar_url)

        message = await ctx.send(embed=embed)

        circles = ["⚫", "🔴", "🟢"]
        for circle in circles:
            await message.add_reaction(circle)

        reaction, user = await self.bot.wait_for(
            "reaction_add",
            check=lambda react, usr: usr == ctx.author and react.message.id == message.id)

        result = circles.index(reaction.emoji) + 1

        winning_number = random.randint(0, 36)
        wygrana = 0

        if result == 1:
            if winning_number in czarne:
                wygrana = bet * 2
        elif result == 2:
            if winning_number in czerwone:
                wygrana = bet * 2
        elif result == 3:
            if winning_number == 0:
                wygrana = bet * 35

        desc = ""
        if winning_number in czarne:
            desc += "Czarna\n"
        elif winning_number in czerwone:
            desc += "Czerwona\n"
        elif winning_number == 0:
            desc += "Zielona"

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
            Baza.add_money(ctx.author.id, wygrana)
            Baza.add_exp(ctx.author.id, wygrana // 10)
        em.set_footer(text=str(ctx.author) + f": +{wygrana}CC, +{wygrana // 10}EXP", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=em)

    @ruletka.error
    async def ruletka_error(self, ctx, error):
        print("RULETKA: ", error)

    @commands.cooldown(3, 60, commands.BucketType.user)
    @commands.command()
    async def zdrapka(self, ctx):
        """ KOSZT ZDRAPKI 5 chillcoinów """

        money = Baza.get_money(ctx.author.id)
        if money < 5:
            return
        else:
            Baza.add_money(ctx.author.id, -5)

        wygrane = {
            0: 57,
            5: 25,
            10: 10,
            20: 5,
            100: 2,
            500: 1,
        }

        wygrana = random.choices(list(wygrane.keys()), weights=list(wygrane.values()))
        wygrana = wygrana[0]

        if wygrana == 0:
            embed = discord.Embed(title="ZDRAPKA", description="Nic nie wygrałeś!", color=discord.Color.red())
        else:
            embed = discord.Embed(title="ZDRAPKA", description=f"Wygrałeś {wygrana} chillcoinów!",
                                  color=discord.Color.green())

        embed.set_footer(text=str(ctx.author), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        Baza.add_money(ctx.author.id, wygrana)

    @zdrapka.error
    async def zdrapka_error(self, ctx, error):
        await ctx.author.send(error)

    # @commands.is_owner()
    # @commands.command()
    # async def splitsteal(self, ctx, amount: int, member1: discord.Member, member2: discord.Member):
    #     sos_embed = discord.Embed(title="Split or Steal?", description="1. Split\n2. Steal",
    #                               color=discord.Color.magenta())
    #
    #     message1 = await member1.send(embed=sos_embed)
    #     await utils.add_digits(message1, 2)
    #
    #     reaction, user = await self.bot.wait_for("reaction_add", check=lambda react,usr: react.message.id == message1.id and usr == member1)
    #     choice1 = utils.get_emoji_value(reaction.emoji)
    #
    #     message2 = await member2.send(embed=sos_embed)
    #     await utils.add_digits(message2, 2)
    #     reaction, user = await self.bot.wait_for("reaction_add", check=lambda react,usr: react.message.id == message2.id and usr == member2)
    #     choice2 = utils.get_emoji_value(reaction.emoji)
    #
    #     if choice1 == choice2:
    #         if choice1 == 1:
    #             await ctx.send(f"Obaj wybraliście SPLIT! Kwota: {amount//2}")
    #         if choice1 == 2:
    #             await ctx.send(f"Obaj wybraliście STEAL! Nic nie wygraliście ;)")
    #     else:
    #         if choice1 == 2:
    #             await ctx.send(f"{str(member1)} ukradłeś wszystko! wygrywasz {amount}")
    #         if choice2 == 2:
    #             await ctx.send(f"{str(member2)} ukradłeś wszystko! wygrywasz {amount}")


def setup(bot):
    bot.add_cog(Kasyno(bot))
