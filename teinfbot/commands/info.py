import discord
from discord.ext import commands


@commands.command()
async def info(ctx: commands.Context, member: discord.Member = None):
    """ Wyświetla informacje o użytkowniku @nick
    jeśli nie podamy użytkownika, to wywołamy na sobie """

    await ctx.message.delete()

    member = member or ctx.message.author
    informacje = {
        "Nick": member.name,
        "ID": member.id,
        "Status": member.status,
        "Najwyższa rola": member.top_role,
        "Dołączył/a": member.joined_at,
        "#": member.discriminator,
        "Avatar": member.avatar_url,
        "Server": member.guild
    }
    wiadomosc = ""
    for key, value in informacje.items():
        wiadomosc += key + " : " + str(value) + "\n"
    em = discord.Embed(
        title=f"Informacje o {informacje['Nick']}", description=wiadomosc, colour=discord.Colour.green())
    await ctx.send(embed=em)


def setup(bot):
    bot.add_command(info)
