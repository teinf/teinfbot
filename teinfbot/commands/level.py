import discord
from discord.ext import commands

from teinfbot.db import db_session
from teinfbot.models import TeinfMember
from teinfbot.utils.levels import LevelsUtils


@commands.command()
async def level(ctx: commands.Context, member: discord.Member = None):
    member = member or ctx.author
    teinf_member: TeinfMember = db_session.query(TeinfMember).filter_by(discordId=member.id).first()
    level = LevelsUtils.levelFromExp(teinf_member.exp)
    next_level_exp = LevelsUtils.expFromLevel(level + 1)
    missing_exp_to_lvlup = next_level_exp - teinf_member.exp

    embed = discord.Embed(
        title="💎 LEVEL 💎",
        description=f"Wykres poziomu {member.mention}\n`{level}LVL - {teinf_member.exp}EXP.`\nBrakuje `{missing_exp_to_lvlup}` do kolejnego poziomu.",
        color=discord.Color.blue()
    )

    embed.set_footer(text=str(ctx.author), icon_url=ctx.author.avatar_url)

    await ctx.send(embed=embed)


def setup(bot):
    bot.add_command(level)
