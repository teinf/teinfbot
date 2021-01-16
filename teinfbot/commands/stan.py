import discord
from discord.ext import commands

from teinfbot import db_session
from teinfbot.models import TeinfMember


@commands.command()
async def stan(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    teinf_member: TeinfMember = db_session.query(TeinfMember).filter_by(discordId=member.id).first()

    embd = discord.Embed(
        title="💵  TEINF BANK  💵",
        description=f"Stan konta {member.mention}:\n`- {teinf_member.money} chillcoinów`",
        color=discord.Color.green()
    )

    await ctx.send(embed=embd)


def setup(bot):
    bot.add_command(stan)
