import discord
import random
from discord.ext import commands
from gtts import gTTS
import gtts


class Zabawa(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def lokieto(self, ctx, *reason):
        to_slap = random.choice(ctx.guild.members)
        slapDescription = '{0.author} walnął z łokieta {1} *{2}*'.format(ctx, to_slap, " ".join(reason))
        em = discord.Embed(title="ŁOKIETO", description=slapDescription, colour=discord.Colour.gold())
        await ctx.send(embed=em)

    @commands.command(name="kutas")
    async def kutas(self, ctx):
        kutas_len = random.randint(1, 30)
        if kutas_len < 10:
            em = discord.Embed(
                title="YELLO DIK",
                description=f"{ctx.author.name} twój mały ma {kutas_len} cm! Współczuję Ci :(",
                colour=discord.Color.gold()
            )
        elif 10 <= kutas_len < 20:
            em = discord.Embed(
                title="WHITE DIK",
                description=f"{ctx.author.name} twój normalny ma {kutas_len} cm! Nadal za mały ale ok",
                colour=discord.Color.from_rgb(255, 255, 255)
            )
        else:
            em = discord.Embed(
                title="BLAKK DIK",
                description=f"{ctx.author.name} twój BBC ma {kutas_len} cm! Witamy in WAKANDA",
                colour=discord.Color.from_rgb(0, 0, 0)
            )

        await ctx.send(embed=em)
        await ctx.message.delete()

    @commands.command()
    async def nyzio(self, ctx):
        alphabet = "ABCDEFGHIJKLMNOPRSTUVWXYZ"
        random_letter = random.choice(alphabet)
        await ctx.send(random_letter + "yzio")

    @commands.command()
    async def say(self, ctx, jezyk, *what):
        """ Użycie: .say en Hello There """
        await ctx.message.delete()
        what = " ".join(what)
        tts = gTTS(what, lang=jezyk)
        file_path = "cogs/musics/music.mp3"
        with open(file_path, 'wb') as f:
            tts.write_to_fp(f)
        await ctx.send(file=discord.File(file_path))


def setup(bot):
    bot.add_cog(Zabawa(bot))
