import discord
import random
from discord.ext import commands


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

        money = self.bot.db.get_member(ctx.author.id, "money")
        if money < bet:
            await ctx.author.send(f"Nie masz wystarczająco pieniędzy - brakuje `{abs(bet - money)}` chillcoinów")
            return

        after_bet_balance = self.bot.db.add_money(ctx.author.id, -bet)

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
            new_balance = self.bot.db.add_money(ctx.author.id, wygrana)
            self.bot.db.add_exp(ctx.author.id, wygrana // 10)
            em.set_footer(text=str(ctx.author) + f": +{wygrana}CC, +{wygrana // 10}EXP, BILANS {new_balance}",
                          icon_url=ctx.author.avatar_url)
        else:
            em.set_footer(text=str(ctx.author) + f":BILANS {after_bet_balance}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=em)

    @ruletka.error
    async def ruletka_error(self, ctx, error):
        print("RULETKA: ", error)

    @commands.cooldown(3, 60, commands.BucketType.user)
    @commands.command()
    # async def zdrapka(self, ctx):
    #     """ KOSZT ZDRAPKI 5 chillcoinów """

    #     money = self.bot.db.get_member(ctx.author.id, "money")
    #     if money < 5:
    #         return
    #     else:
    #         self.bot.db.add_money(ctx.author.id, -5)

    #     wygrane = {
    #         0: 57,
    #         5: 25,
    #         10: 10,
    #         20: 5,
    #         100: 2,
    #         500: 1,
    #     }

    #     wygrana = random.choices(list(wygrane.keys()), weights=list(wygrane.values()))
    #     wygrana = wygrana[0]

    #     if wygrana == 0:
    #         embed = discord.Embed(title="ZDRAPKA", description=f"{ctx.author} nic nie wygrałeś!",
    #                               color=discord.Color.red())
    #     else:
    #         embed = discord.Embed(title="ZDRAPKA", description=f"{ctx.author} wygrałeś {wygrana} chillcoinów!",
    #                               color=discord.Color.green())

    #     new_balance = self.bot.db.add_money(ctx.author.id, wygrana)
    #     embed.set_footer(text=f"Nowy bilans: {new_balance}", icon_url=ctx.author.avatar_url)
    #     self.bot.db.add_exp(ctx.author.id, wygrana // 5)
    #     await ctx.send(embed=embed)

    # @zdrapka.error
    # async def zdrapka_error(self, ctx, error):
    #     await ctx.author.send(error)

    # @commands.cooldown(1, 86400, commands.BucketType.user)
    # @commands.command()
    async def daily_zdrapka(self, ctx):
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

        new_balance = self.bot.db.add_money(ctx.author.id, wygrana)

        if wygrana == 0:
            embed = discord.Embed(
                title="DAILY ZDRAPKA",
                description=f"{ctx.author} nic nie wygrałeś!",
                color=discord.Color.red()
            )
        else:
            embed = discord.Embed(
                title="DAILY ZDRAPKA",
                description=f"{ctx.author} wygrałeś {wygrana} chillcoinów!",
                color=discord.Color.green()
            )

        embed.set_footer(text=f"Nowy bilans: {new_balance}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @daily_zdrapka.error
    async def daily_zdrapka_error(self, ctx, error):
        await ctx.author.send(error)


def setup(bot):
    bot.add_cog(Kasyno(bot))
