import discord
from discord.ext import commands
from teinfbot import db

class Kasa(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def get_user(self, ctx, member: discord.Member):
        await ctx.send(db.get_member_info(str(member.id)))

    @commands.is_owner()
    @commands.command()
    async def add_money(self, ctx, member: discord.Member, amount: int):
        new_balance = db.add_money(str(member.id), amount)
        embd = discord.Embed(
            title="💵  TEINF BANK  💵",
            description=f"Nowy stan konta {member.mention}:\n`- {new_balance} chillcoinów`",
            color=discord.Color.green()
        )
        await ctx.send(embed=embd)

    @commands.is_owner()
    @commands.command()
    async def add_exp(self, ctx, member: discord.Member, amount: int):
        new_balance = db.add_exp(str(member.id), amount)
        embd = discord.Embed(
            title="💵  TEINF BANK  💵",
            description=f"Dodano {amount} EXP dla {ctx.author.mention}",
            color=discord.Color.green()
        )
        await ctx.send(embed=embd)

    @commands.command()
    async def stan(self, ctx):
        balance = db.get_member(str(ctx.author.id), "money")
        embd = discord.Embed(
            title="💵  TEINF BANK  💵",
            description=f"Stan konta {ctx.author.mention}:\n`- {balance} chillcoinów`",
            color=discord.Color.green()
        )

        await ctx.send(embed=embd)

    @commands.command()
    async def level(self, ctx: commands.Context):
        exp, level = db.get_member(str(ctx.author.id), "exp", "level")
        missing_exp_to_lvlup = int(exp - (level * 110))
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
        level = db.get_member(str(ctx.author.id), "level")
        daily_amount = level * 10
        new_balance = db.add_money(ctx.author.id, daily_amount)

        embd = discord.Embed(
            title="💵 TEINF BANK 💵",
            description=f"{ctx.author.mention}, dostajesz {daily_amount} chillcoinsów\n"
                        f"Nowy stan konta: `{new_balance} CC`",
            color=discord.Color.green()
        )
        await ctx.send(embed=embd)

    @daily.error
    async def daily_error(self, ctx, error):
        await ctx.author.send(error)


def setup(bot):
    bot.add_cog(Kasa(bot))
