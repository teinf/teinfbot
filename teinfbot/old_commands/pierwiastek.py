from discord.ext import commands


def rozklad(n):
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


@commands.command()
async def pierwiastek(ctx: commands.Context, *args):
    if len(args) == 0:
        await ctx.send("Musisz podać liczbę! : .pierwiastek <liczba> <liczba2> ...")
    else:
        msg = "\n".join((arg + ": " + (rozklad(int(arg))) for arg in args if int(arg) >= 0))
        await ctx.send(msg)


def setup(bot):
    bot.add_command(pierwiastek)
