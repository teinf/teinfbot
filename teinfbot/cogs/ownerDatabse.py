import math

import discord
from discord.ext import commands

from teinfbot import db
from teinfbot.models import TeinfMember

LEVEL_MULTIPLIER = 0.15


class Kasa(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def get_user(self, ctx, member: discord.Member):
        await ctx.send(db.get_member_info(str(member.id)))

    @commands.is_owner()
    @commands.command()
    async def add_money(self, ctx, member: discord.Member, amount: int):
        teinf_member: TeinfMember = db.session.query(TeinfMember).filter_by(discordId=member.id).first()
        teinf_member.money += amount

        embd = discord.Embed(
            title="💵  TEINF BANK  💵",
            description=f"Nowy stan konta {member.mention}:\n`- {teinf_member.money} chillcoinów`",
            color=discord.Color.green()
        )
        await ctx.send(embed=embd)

    @commands.is_owner()
    @commands.command()
    async def add_exp(self, ctx, member: discord.Member, amount: int):
        teinf_member: TeinfMember = db.session.query(TeinfMember).filter_by(discordId=member.id).first()
        teinf_member.money += amount

        embd = discord.Embed(
            title="💵  TEINF BANK  💵",
            description=f"Dodano {amount} EXP dla {ctx.author.mention}",
            color=discord.Color.green()
        )
        await ctx.send(embed=embd)

    @commands.command()
    async def stan(self, ctx, member: discord.Member = None):
        member = member or ctx.author.id
        teinf_member: TeinfMember = db.session.query(TeinfMember).filter_by(discordId=member.id).first()

        embd = discord.Embed(
            title="💵  TEINF BANK  💵",
            description=f"Stan konta {member.mention}:\n`- {teinf_member.money} chillcoinów`",
            color=discord.Color.green()
        )

        await ctx.send(embed=embd)

    @staticmethod
    def level_from_exp(exp: int):
        if exp == 0:
            return 0

        return int(LEVEL_MULTIPLIER * math.sqrt(exp))

    @staticmethod
    def exp_from_level(level: int):
        return int(level * level * (1 / LEVEL_MULTIPLIER) * (1 / LEVEL_MULTIPLIER))

    @commands.command()
    async def level(self, ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author.id
        teinf_member: TeinfMember = db.session.query(TeinfMember).filter_by(discordId=member.id).first()
        level = self.level_from_exp(teinf_member.exp)
        next_level_exp = self.exp_from_level(level + 1)
        missing_exp_to_lvlup = next_level_exp - teinf_member.exp

        embed = discord.Embed(
            title="💎 LEVEL 💎",
            description=f"Wykres poziomu {member.mention}\n`{level}LVL - {teinf_member.exp}EXP.`\nBrakuje `{missing_exp_to_lvlup}` do kolejnego poziomu.",
            color=discord.Color.blue()
        )

        embed.set_footer(text=str(ctx.author), icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        teinf_member: TeinfMember = db.session.query(TeinfMember).filter_by(discordId=ctx.author.id).first()
        level = self.level_from_exp(teinf_member.exp)
        daily_amount = level * 10
        teinf_member.money += daily_amount

        embd = discord.Embed(
            title="💵 TEINF BANK 💵",
            description=f"{ctx.author.mention}, dostajesz {daily_amount} chillcoinsów\n"
                        f"Nowy stan konta: `{teinf_member.money} CC`",
            color=discord.Color.green()
        )
        await ctx.send(embed=embd)

    @daily.error
    async def daily_error(self, ctx, error):
        await ctx.author.send(error)


def setup(bot):
    bot.add_cog(Kasa(bot))
