import discord
import asyncio
import random
import datetime
import json
from discord.ext import commands


class Narzedzia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        """ Wyświetla link z obrazem użtykownika @nick
        jeśli nie podamy użytkownika, to wywołamy na sobie """
        member = member or ctx.message.author
        await ctx.send(f"{member.avatar_url}", delete_after=20)

    @commands.command()
    async def info(self, ctx, member: discord.Member = None):
        """ Wyświetla informacje o użytkowniku @nick
        jeśli nie podamy użytkownika, to wywołamy na sobie """
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
            #print(key, ":", value)
            wiadomosc += key + " : " + str(value) + "\n"
        # wiadomosc = "```py\nNick: {0.name}\nID: {0.id}\nStatus: {0.status}\nNajwyższa rola: {0.top_role}\nDołączył/a: {0.joined_at}\n#: {0.discriminator}\nAvatar: {0.avatar_url}\nCo robi aktualnie: {0.activities}\nServer: {0.guild}```"
        em = discord.Embed(
            title=f"Informacje o {informacje['Nick']}", description=wiadomosc, colour=discord.Colour.green())
        await ctx.send(embed=em, delete_after=20)

    @commands.command()
    async def pobudka(self, ctx):
        """ Pokazuje o której powinniśmy wstać jeśli pójdziemy spać teraz """
        dateTimeNow = datetime.datetime.now()

        def jumpSleepCycle(amount=1):
            sleepCycle = datetime.timedelta(hours=1, minutes=30)
            avgTimeToFallAsleep = datetime.timedelta(minutes=15)
            return dateTimeNow + sleepCycle*int(amount) + avgTimeToFallAsleep

        strHourAndMinutes = "**`{0.hour:02d}:{0.minute:02d}`**"

        wakeUpHours = []
        for i in range(1, 7):
            formattedStr = strHourAndMinutes.format(jumpSleepCycle(i))
            wakeUpHours.append(formattedStr)

        str_wake_up_hours = " lub ".join(wakeUpHours)
        await ctx.send(f"{ctx.message.author.mention} jeśli chciałbyś iść teraz spać to \npowinienieś ustawić budzik na te godziny: \n{str_wake_up_hours}")

    @commands.command(aliases=["alarm"])
    async def budzik(self, ctx, hour: int = 7, minutes: int = 0, *args):
        """ Gdy podamy godzinę o której chcemy wstać to pokazuje
         o której godzinie powinniśmy pójść spać np. .budzik 7 30 """
        alarm_time = datetime.timedelta(hours=hour, minutes=minutes)

        def jump_sleep_cycle(amount=1):
            sleep_cycle = datetime.timedelta(hours=1, minutes=30)
            avg_time_to_fall_asleep = datetime.timedelta(minutes=15)
            return alarm_time - sleep_cycle*int(amount) - avg_time_to_fall_asleep

        def convert_time_delta_to_dhm(td):
            """Converts timedelta to days, hours, minutes"""
            return td.days, td.seconds//3600, (td.seconds//60) % 60

        str_hour_and_minutes = "**`{0:02}:{1:02}`**"

        go_to_bed_hours = []
        for i in range(2, 7):
            td_days, td_hours, td_minutes = convert_time_delta_to_dhm(
                jump_sleep_cycle(i))
            formatted_str = str_hour_and_minutes.format(td_hours, td_minutes)
            go_to_bed_hours.append(formatted_str)
            del td_days

        str_go_to_bed_hours = " lub ".join(reversed(go_to_bed_hours))
        await ctx.send(f"{ctx.message.author.mention} aby wstać o {str_hour_and_minutes.format(hour,minutes)} powinienieś położyć się do łóżka o \n{str_go_to_bed_hours}")

def setup(bot):
    bot.add_cog(Narzedzia(bot))
