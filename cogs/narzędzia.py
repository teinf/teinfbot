import discord
import asyncio
import random
import datetime
import json
from discord.ext import commands


class Narzedzia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()  # wyświetla link z obrazem użtykownika @nick, jeśli member pusty = "None" to wywołamy na autorze wiadomości
    async def avatar(self, ctx, member: discord.Member = None):
        member = member or ctx.message.author
        await ctx.send(f"{member.avatar_url}", delete_after=20)

    @commands.command()  # wyświetla informacje o danym użytkowniku @nick, jeśli member = "None" to wywołamy na autorze wiadomości
    async def info(self, ctx, member: discord.Member = None):
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

        strWakeUpHours = " lub ".join(wakeUpHours)
        await ctx.send(f"{ctx.message.author.mention} jeśli chciałbyś iść teraz spać to \npowinienieś ustawić budzik na te godziny: \n{strWakeUpHours}")

    @commands.command(aliases=["alarm"])
    async def budzik(self, ctx, hour: int = 7, minutes: int = 0, *args):

        alarmTime = datetime.timedelta(hours=hour, minutes=minutes)

        def jumpSleepCycle(amount=1):
            sleepCycle = datetime.timedelta(hours=1, minutes=30)
            avgTimeToFallAsleep = datetime.timedelta(minutes=15)
            return alarmTime - sleepCycle*int(amount) - avgTimeToFallAsleep

        def convertTimeDeltaToDHM(td):
            """Converts timedelta to days, hours, minutes"""
            return td.days, td.seconds//3600, (td.seconds//60) % 60

        strHourAndMinutes = "**`{0:02}:{1:02}`**"

        GoToBedHours = []
        for i in range(2, 7):
            td_days, td_hours, td_minutes = convertTimeDeltaToDHM(
                jumpSleepCycle(i))
            formattedStr = strHourAndMinutes.format(td_hours, td_minutes)
            GoToBedHours.append(formattedStr)
            del td_days

        strGoToBedHours = " lub ".join(reversed(GoToBedHours))
        await ctx.send(f"{ctx.message.author.mention} aby wstać o {strHourAndMinutes.format(hour,minutes)} powinienieś położyć się do łóżka o \n{strGoToBedHours}")

    @commands.command()
    async def kurs(self, ctx, nominal=None, amount=10):
        with open('cogs/txt/currency.json', 'r') as f:
            currencies = json.load(f)

        if nominal == None:
            nominalsList = [nominalStr for nominalStr in currencies]
            # EUR : Euro

            em = discord.Embed(
                title=":moneybag: DOSTĘPNE WALUTY :moneybag:", colour=discord.Colour.gold())

            for curr in nominalsList:
                nominal = currencies.get(curr)

                CODE = nominal['code']
                NAME = nominal['name']
                RATE = round(nominal['inverseRate'], 2)

                moneyCantor = "{0}\n1 {1} = {2} PLN"
                em.add_field(name=CODE.upper(), value=moneyCantor.format(
                    NAME, CODE, RATE), inline=True)
            await ctx.send(embed=em, delete_after=30)
        else:
            moneyToConvert = currencies.get(nominal.lower())
            convertRate = moneyToConvert['inverseRate']
            convertedMoney = round(amount * convertRate, 2)

            convertStr = f"{amount} {moneyToConvert['code']} = {convertedMoney} PLN"
            em = discord.Embed(title=":moneybag: KURS WALUT :moneybag:",
                               description=convertStr, colour=discord.Colour.gold())
            await ctx.send(embed=em, delete_after=30)

    @commands.command()
    async def plan(self, ctx, *, weekDay=None):

        await ctx.message.delete()

        with open("cogs/txt/planLekcji.json", 'r', encoding='utf-8') as f:
            timetable = json.load(f)

        weekDays = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek"]
        lessonHours = {
            1: '08:15 - 09:00',
            2: '09:05 - 09:50',
            3: '09:55 - 10:40',
            4: '10:45 - 11:30',
            5: '11:45 - 12:30',
            6: '12:35 - 13:20',
            7: '13:25 - 14:10',
            8: '14:30 - 15:15',
            9: '15:20 - 16:05'
        }

        if weekDay != None:
            if weekDay not in weekDays:
                weekDay = None

        if weekDay == None:
            weekDay = datetime.datetime.today().weekday()
            weekDay += 1
            if weekDay <= 0 or weekDay >= 6:
                weekDay = 0
            weekDay = weekDays[weekDay]

        def dayPlanStr(dzienTygodnia):
            lessonStrFormula = "{0[name]} : **`{0[sala]}`** \n **{0[nauczycielskr]}** - {0[nauczyciel]}\n\n"
            timetableDay = timetable.get(dzienTygodnia)
            hourLessonFormula = "**{0}** : **`{1}`**\n"
            dayPlan = ""
            if dzienTygodnia == "Czwartek" or dzienTygodnia == "Piątek":
                for i in range(2, len(timetableDay)+1):
                    dayPlan += hourLessonFormula.format(
                        i+1, lessonHours[i+1]) + lessonStrFormula.format(timetableDay[str(i+1)])
            else:
                for i in range(len(timetableDay)):
                    dayPlan += hourLessonFormula.format(
                        i+1, lessonHours[i+1]) + lessonStrFormula.format(timetableDay[str(i+1)])
            return dayPlan

        for day in weekDays:
            if weekDay == day:
                planStr = dayPlanStr(day)

        em = discord.Embed(
            title=f"PLAN LEKCJI - {weekDay.upper()}", description=planStr, colour=discord.Colour.green())
        await ctx.send(embed=em, delete_after=60)

    @commands.command()
    async def szyfruj(self, ctx, *slowo):
        await ctx.message.delete()
        slowa = " ".join(slowo)
        alfabet = "aąbcćdeęfghijklłmnńoóprsśtuwyzźż"
        znaki_specjalne = "!@#$%^&*(-="

        # TWORZENIE TAKICH HASEŁ
        doKonwersji = slowa
        doKonwersji.lower().replace(" ", "")

        haslo = ""
        suma_znakow = 0
        for i, znak in enumerate(doKonwersji):
            suma_znakow += alfabet.find(znak) + 1
            if i % 6 == 0:
                haslo += znak.lower()
            elif i % 6 == 1:
                haslo += str(suma_znakow)
            elif i % 6 == 2:
                haslo += znak.upper()
            elif i % 6 == 3:
                haslo += str(alfabet.find(znak) + 1)
            elif i % 6 == 4:
                haslo += znaki_specjalne[(alfabet.find(znak) + 1) % 11]
            elif i % 6 == 5:
                haslo += str(alfabet[abs((alfabet.find(znak) + 1) - 32)])
        em = discord.Embed(title=f"SZYFR", description=haslo,
                           colour=discord.Colour.red())
        await ctx.send(embed=em, delete_after=30)


def setup(bot):
    bot.add_cog(Narzedzia(bot))
