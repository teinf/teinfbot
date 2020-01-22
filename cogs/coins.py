import discord
from discord.ext import commands
from waluta import Baza


class Coins(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def bilans(self, ctx: commands.Context, memb: discord.Member = None):
        if memb is None:
            embed = discord.Embed(
                title="💰 BILANS KONTA 💰",
                description=f"`BILANS = {Baza.get_money(ctx.author.id)}cc`",
                color=discord.Color.dark_green()
            )

            embed.set_footer(text=str(ctx.author), icon_url=ctx.author.avatar_url)

            await ctx.send(embed=embed)
        else:
            baza_info = Baza.get_member(memb.id)
            embed = discord.Embed(
                title="💵 BILANS KONTA 💵",
                description=f"Bilans {memb.mention}\n{Baza.get_money(memb.id)} CC.",
                color=discord.Color.dark_green()
            )

            embed.set_footer(text=str(memb), icon_url=memb.avatar_url)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def add_money(self, ctx: commands.Context, member: discord.Member, amount: int):
        await ctx.send(f"Dano {amount}CC dla {member.mention}")
        Baza.add_money(member.id, amount)

    @commands.command()
    async def level(self, ctx: commands.Context):
        exp = Baza.get_exp(ctx.author.id)
        level = Baza.get_level(ctx.author.id)
        missing_exp_to_lvlup = int(exp - (level * 1.1 * 100))
        missing_exp_to_lvlup = abs(missing_exp_to_lvlup)

        embed = discord.Embed(
            title="💎 LEVEL 💎",
            description=f"Wykres poziomu {ctx.author.mention}\n`{level}LVL - {exp}EXP.`\nBrakuje `{missing_exp_to_lvlup}` do kolejnego poziomu.",
            color=discord.Color.blue()
        )

        embed.set_footer(text=str(ctx.author), icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        level = Baza.get_level(ctx.author.id)
        daily_amount = level * 10
        Baza.add_money(ctx.author.id, daily_amount)
        await ctx.send(f"{ctx.author.mention}, dostajesz {daily_amount} chillcoinsów")

    @daily.error
    async def daily_error(self, ctx, error):
        await ctx.author.send(error)

    # @commands.command()
    # async def ranking(self, ctx):
    #     top = Baza.get_top(3)
    #     users = ""
    #     for i, (id, money, exp, level) in enumerate(top):
    #         usr = self.bot.get_user(id)
    #         users += str(usr)+"\n"
    #     await ctx.send(users)


def setup(bot):
    bot.add_cog(Coins(bot))
