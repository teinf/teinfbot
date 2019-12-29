import discord
import asyncio
import random
import json
from discord.ext import commands
from discord import File


class Zabawa(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()  # robi wahadło na gościu @nick normalnie, robi to num (domyslnie 5) razy, jeśli member pusty = "None" to wywołamy na autorze wiadomości
    @commands.cooldown(1, 60, commands.BucketType.default)
    async def wahadlo(self, ctx, member: discord.Member = None, num: int = 3):

        # kiedy member=None to wybiera drugą opcje - ctx.message.author
        member = member or ctx.message.author

        try:
            # Zapisuje obecny kanał głosowy, na którym jest
            current_channel = member.voice.channel
        except Exception as e:
            print(e)

        # uzyskanie informacji o wahadlo1
        channel1 = self.bot.get_channel(535131761634705408)
        # uzyskanie informacji o wahadlo2
        channel2 = self.bot.get_channel(535131819192877066)

        await ctx.message.delete()  # usunięcie wiadomosci ".wahadlo"

        em = discord.Embed(title="\u26A1 WAHADŁO \u26A1",
                           description=f"ROBIMY WAHADŁO NA **{member}** ?", colour=discord.Colour.orange())
        em.set_footer(text="*KLIKNIJ* \u2705")
        new_message = await ctx.send(embed=em)

        # dodanie emotki ✅ pod wiadomością
        await new_message.add_reaction('\u2705')

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) == '\u2705'

        try:
            # wait for 1 argument przyjmuje wartosci on_reaction_add
            await self.bot.wait_for('reaction_add', timeout=10.0, check=check)

        except asyncio.TimeoutError:
            await ctx.send("Koniec czasu!")

        else:  # jeśli nie except
            # musimy odświeżyć informacje na temat reakcji
            new_message = await ctx.get_message(new_message.id)
            reaction = new_message.reactions[0]

            # print([user.name for user in await reaction.users().flatten()].remove("TEINF")) # zamiana reaction.users() na liste za pomocą flatten() i dodanie user.name do listy oraz usunięcie z niej bota "TEINF"

            # await ctx.send(new_message.reactions[0].count) # liczy ilość 1 reakcji dodanej

            # dopóki są 2+ ✅ reakcje pod wiadomością
            while new_message.reactions[0].count >= 2:
                await member.move_to(channel1)
                await member.move_to(channel2)
                await asyncio.sleep(1.5)
                # odświeżenie informacji na temat reakcji
                new_message = await ctx.get_message(new_message.id)

            await new_message.delete()  # usuwanie wiadomości
            await member.move_to(current_channel)

    @commands.command()
    async def lokieto(self, ctx, *reason):
        to_slap = random.choice(ctx.guild.members)
        slapDescription = '{0.author} walnął z łokieta {1} bo *{2}*'.format(ctx, to_slap, " ".join(reason))
        em = discord.Embed(title = "ŁOKIETO", description= slapDescription, colour= discord.Colour.gold())
        await ctx.send(embed = em)

    @commands.command(aliases=["losowy_cytat", "cytacik", "cytat"])
    async def cytaty(self, ctx):
        with open("cogs/txt/cytaty.json", 'r', encoding="UTF-8") as f:
            cites = json.load(f)

        imie, losowy_cytat = random.choice(list(cites.items()))
        losowy_cytat = random.choice(losowy_cytat)

        em = discord.Embed(title=imie, description=losowy_cytat,
                           colour=discord.Colour.blurple())
        await ctx.send(embed=em, delete_after=30)
        await ctx.message.delete()

    @commands.command(aliases=["+cytat", "cytat+"])
    async def dodaj_cytat(self, ctx, name, *cite):
        """ .cytat+ <imie> <cytat> """
        with open("cogs/txt/cytaty.json", 'r', encoding="UTF-8") as f:
            cites = json.load(f)

        cite = " ".join(cite)
        if not name in cites:
            cites[name] = []

        cites[name].append(cite)

        with open("cogs/txt/cytaty.json", 'w', encoding="UTF-8") as f:
            json.dump(cites, f, ensure_ascii=False)

        await ctx.message.delete()
        await ctx.send("**` POMYŚLNIE DODANO CYTAT `**", delete_after=10)

    @commands.command(aliases=["penis", "chuj"])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def kutas(self, ctx):
        losowa = random.choice(range(1, 30))
        if losowa < 10:
            kolor = discord.Colour.gold()
            znak = "tylko"
        elif 10 <= losowa < 20:
            kolor = discord.Colour.from_rgb(255, 255, 255)
            znak = ""
        elif 20 <= losowa <= 30:
            kolor = discord.Colour.from_rgb(0, 0, 0)
            znak = "aż"

        await ctx.send("Przykłada chuja do linijki...", delete_after=5)

        em = discord.Embed(title="\U0001F51E Kutas \U0001F51E",
                           description=f'{ctx.message.author} Twój kutas ma {znak} **{losowa}** cm', colour=kolor)
        await ctx.send(embed=em, delete_after=20)
        await ctx.message.delete()

    @commands.command(aliases=["rasy"])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def rasa(self, ctx):
        with open("cogs/txt/rasy.txt", 'r', encoding="UTF-8") as f:
            rasy = [line.strip() for line in f]
        losowa_rasa = random.choice(rasy)
        em = discord.Embed(
            title="RASA", description=f"{ctx.message.author} twoja rasa to {losowa_rasa}", colour=discord.Colour.blue())
        await ctx.send(embed=em, delete_after=20)
        await ctx.message.delete()

    @commands.command()
    async def nyzio(self, ctx):
        alphabet = "A B C D E F G H I J K L M N O P R S T U V W X Y Z"
        alphabetLs = alphabet.split(" ")
        randomLetter = random.choice(alphabetLs)
        await ctx.send(randomLetter + "yzio")

    # @commands.command()
    # async def powiedz(self, ctx, jezyk, *what):
    #     await ctx.message.delete()
    #     what = " ".join(what)
    #     from discord import File
    #     tts = gTTS(what, lang=jezyk)
    #     with open(r"P:\Projekty\Discord Bots\TEINF BOT\cogs\musics\music.mp3", 'wb') as f:
    #         tts.write_to_fp(f)
    #     await ctx.send(file=File(r"P:\Projekty\Discord Bots\TEINF BOT\cogs\musics\music.mp3"))


def setup(bot):
    bot.add_cog(Zabawa(bot))
