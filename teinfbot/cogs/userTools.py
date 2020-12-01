from typing import List

import discord
from discord.ext import commands
from teinfbot import db
from teinfbot.models import TeinfMember

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
        await ctx.send(f"{member.display_name} spędził {teinfMember.timespent // 60:02d}:{teinfMember.timespent%60:02d} na serwerze")

    @commands.command()
    async def czasTop(self, ctx, amount: int = 5):
        await ctx.message.delete()

        topTimeSpentMembers: List[TeinfMember] = db.session.query(TeinfMember).order_by(TeinfMember.timespent).all()
        i = 1
        for member in topTimeSpentMembers[::-1]:
            discordMember: discord.Member = self.bot.get_user(member.discordId)
            if not discordMember:
                continue

            if i > amount:
                break
            displayName = discordMember.display_name
            await ctx.send(f"{i}.{displayName} - {}{member.timespent // 60:02d}:{member.timespent%60:02d}")
            i+=1

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
