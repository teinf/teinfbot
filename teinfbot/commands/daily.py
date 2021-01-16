from discord.ext import commands
import discord

from teinfbot.models import TeinfMember
from teinfbot import db_session
from teinfbot.utils.levels import LevelsUtils

@commands.command()
@commands.cooldown(1, 86400, commands.BucketType.user)
async def daily(ctx):
    teinf_member: TeinfMember = db_session.query(TeinfMember).filter_by(discordId=ctx.author.id).first()
    level = LevelsUtils.levelFromExp(teinf_member.exp)
    daily_amount = (level + 1) * 10
    teinf_member.money += daily_amount

    embd = discord.Embed(
        title="💵 TEINF BANK 💵",
        description=f"{ctx.author.mention}, dostajesz {daily_amount} chillcoinsów\n"
                    f"Nowy stan konta: `{teinf_member.money} CC`",
        color=discord.Color.green()
    )
    await ctx.send(embed=embd)


@daily.error
async def daily_error(ctx, error):
    await ctx.author.send(error)
def setup(bot):
    bot.add_command(daily)
