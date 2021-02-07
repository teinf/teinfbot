import discord
from discord.ext import commands


def pierwiastek(n):
    dzielniki = {}

    while n > 1:
        for i in range(2, n+1):
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
        lewaStrona *= (dzielnik ** (dzielniki[dzielnik]//2))
        prawaStrona *= (dzielnik ** (dzielniki[dzielnik]%2))

    znakPierwiastka = u"\u221a"
    if prawaStrona != 1:
        return str(lewaStrona) + znakPierwiastka + str(prawaStrona)
    else:
        return str(lewaStrona)


@commands.command()
async def pierwiastek(ctx: commands.Context, *args):
    if len(args) == 0:
        await ctx.send("Musisz podać liczbę! : .pierwiastek <liczba> <liczba2> ...")
    else:
        msg = " ".join((pierwiastek(int(arg)) for arg in args if int(arg) >= 0))
        await ctx.send(msg)


