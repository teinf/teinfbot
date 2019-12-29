import discord,asyncio, random, json
from discord.ext import commands
from discord.ext.commands import Bot

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True,aliases=["champion_lol","champ_lol",'lolchamp','lol_champion','lol'], name="liga")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def lol_champ(self,ctx):
        with open("cogs/txt/lol_postacie.txt") as f:
            champs = [line.strip() for line in f]

        random_champ = random.choice(champs)
        random_champ = random_champ.replace('\'', "").replace(" ", "").replace(".", "")

        stupid_champs = ["ChoGath","KaiSa","KhaZix"]
        if random_champ in stupid_champs:
            random_champ = random_champ.title()

        champ_image_url = "https://ddragon.leagueoflegends.com/cdn/9.1.1/img/champion/{}.png".format(random_champ)

        em = discord.Embed(title=random_champ, description= ctx.message.author.mention, colour=discord.Colour.gold())
        em.set_image(url=champ_image_url)
        await ctx.send(embed = em, delete_after=20)

    @commands.command(pass_context=True, name="r6")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def r6_champ(self,ctx,side=random.choice(["Atak","Obrona"])):
        with open('cogs/txt/rs6_postacie_atak.json', 'r', encoding='utf-8') as f:
            rs6_atak = json.load(f)
        with open('cogs/txt/rs6_postacie_obrona.json', 'r', encoding='utf-8') as f:
            rs6_obrona = json.load(f)
        if side.lower() in ["a",'atak','atk']:
            losowy_champ, losowy_champ_url = random.choice(list(rs6_atak.items()))
            kolor = discord.Colour.orange()
        else:
            losowy_champ, losowy_champ_url = random.choice(list(rs6_obrona.items()))
            kolor = discord.Colour.blue()

        em = discord.Embed(title=losowy_champ,description=ctx.message.author.mention, colour= kolor)
        await ctx.message.delete()
        em.set_image(url=losowy_champ_url)

        await ctx.send(embed=em,delete_after=20)

def setup(bot):
    print("LOADED COGS/GAMES")
    bot.add_cog(Games(bot))
