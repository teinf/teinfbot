from datetime import timedelta
from typing import List

import discord
from discord.ext import commands

from teinfbot import db_session
from teinfbot.models import TeinfMember


class UserTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def getTimeInfo(self, minutes: int):
        delta = timedelta(minutes=minutes)
        deltaStr = str(delta).replace("days", "dni").replace("day", "dzień")[:-3]
        return deltaStr

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        """ Wyświetla link z obrazem użtykownika @nick
        jeśli nie podamy użytkownika, to wywołamy na sobie """

        await ctx.message.delete()

        member = member or ctx.message.author
        await ctx.send(f"{member.avatar_url}")

    @commands.command()
    async def czas(self, ctx, member: discord.Member = None):
        await ctx.message.delete()

        member = member or ctx.message.author

        teinfMember: TeinfMember = db_session.query(TeinfMember).filter_by(discordId=member.id).first()

        em = discord.Embed(
            title="Czas spędzony na serwerze",
            description=f"{member.display_name} spędził {self.getTimeInfo(teinfMember.timespent)} na serwerze",
            color=discord.Colour.green()
        )
        await ctx.send(embed=em)

    @commands.command()
    async def czasTop(self, ctx, amount: int = 5):
        await ctx.message.delete()

        topTimeSpentMembers: List[TeinfMember] = db_session.query(TeinfMember).order_by(TeinfMember.timespent).all()
        i = 1

        topkaTitle = "TOP CZASU"
        topkaDescription = ""

        for member in topTimeSpentMembers[::-1]:
            if i > amount:
                break

            mention = f"<@{member.discordId}>"

            topkaDescription += f"{i}. {mention:15} {self.getTimeInfo(member.timespent)}\n"
            i += 1

        em = discord.Embed(
            title=topkaTitle,
            description=topkaDescription,
            color=discord.Color.gold()
        )

        await ctx.send(embed=em)

    @commands.command()
    async def info(self, ctx, member: discord.Member = None):
        """ Wyświetla informacje o użytkowniku @nick
        jeśli nie podamy użytkownika, to wywołamy na sobie """

        await ctx.message.delete()

        member = member or ctx.message.author
        informacje = {  # key : value,
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
            # print(key, ":", value)
            wiadomosc += key + " : " + str(value) + "\n"
        # wiadomosc = "```py\nNick: {0.name}\nID: {0.id}\nStatus: {0.status}\nNajwyższa rola: {0.top_role}\nDołączył/a: {0.joined_at}\n#: {0.discriminator}\nAvatar: {0.avatar_url}\nCo robi aktualnie: {0.activities}\nServer: {0.guild}```"
        em = discord.Embed(
            title=f"Informacje o {informacje['Nick']}", description=wiadomosc, colour=discord.Colour.green())
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(UserTools(bot))
