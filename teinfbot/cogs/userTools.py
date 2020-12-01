from typing import List

import discord
from discord.ext import commands
from teinfbot import db
from teinfbot.models import TeinfMember
from datetime import datetime

class MinutesTime:
    def __init__(self, minutes: int):
        self.minutes = minutes%60
        self.hours = minutes//60
        self.days = self.hours//24
        self.months = self.hours//30
        self.years = self.months//12

class UserTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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

        teinfMember: TeinfMember = db.session.query(TeinfMember).filter_by(discordId = member.id).first()
        minutesFromTime = MinutesTime(teinfMember.timespent)

        em = discord.Embed(
            title="Czas spędzony na serwerze",
            description=f"{member.display_name} spędził {minutesFromTime.days} dni, {minutesFromTime.hours} godzin i {minutesFromTime.minutes} minut na serwerze",
            color=discord.Colour.green()
        )
        await ctx.send(embed=em)

    @commands.command()
    async def czasTop(self, ctx, amount: int = 5):
        await ctx.message.delete()

        topTimeSpentMembers: List[TeinfMember] = db.session.query(TeinfMember).order_by(TeinfMember.timespent).all()
        i = 1

        topkaTitle = "TOP CZASU"
        topkaDescription = ""

        for member in topTimeSpentMembers[::-1]:
            discordMember: discord.Member = self.bot.get_user(member.discordId)
            if not discordMember:
                continue

            if i > amount:
                break
            displayName = discordMember.display_name

            minutesFromTime = MinutesTime(member.timespent)
            topkaDescription += f"{discordMember.display_name}:{minutesFromTime.days}d, {minutesFromTime.hours}h"
            i+=1

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
