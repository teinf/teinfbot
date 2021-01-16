import os

from discord.ext import commands
import discord

from teinfbot import TeinfBot
from teinfbot.paths import COGS_PATH
from teinfbot import db_session
from teinfbot.models import TeinfMember, Tranzakcje
from teinfbot.utils.levels import LevelsUtils



class Owner(commands.Cog):
    def __init__(self, bot: TeinfBot):
        self.bot = bot

    async def reload_extension(self, ctx, extension):
        try:
            self.bot.reload_extension(extension)
        except Exception as e:
            pass
        finally:
            await ctx.channel.send(f"Pomyślnie załadowano {extension}", delete_after=30)

    @commands.is_owner()
    @commands.command()
    async def reload(self, ctx: commands.Context, extension: str = None):
        if extension:
            await self.reload_extension(ctx, extension)
        else:
            extensions = [cog.split(".")[0] for cog in os.listdir(COGS_PATH) if cog.endswith(".py")]
            for extension in extensions:
                await self.reload_extension(ctx, extension)

    @commands.is_owner()
    @commands.command()
    async def add_money(self, ctx, member: discord.Member, amount: int):
        teinf_member: TeinfMember = db_session.query(TeinfMember).filter_by(discordId=member.id).first()
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
        teinf_member: TeinfMember = db_session.query(TeinfMember).filter_by(discordId=member.id).first()
        teinf_member.money += amount

        embd = discord.Embed(
            title="💵  TEINF BANK  💵",
            description=f"Dodano {amount} EXP dla {ctx.author.mention}",
            color=discord.Color.green()
        )
        await ctx.send(embed=embd)


def setup(bot):
    bot.add_cog(Owner(bot))
