import discord
from discord.ext import commands
from waluta import Baza


class Coins(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def bilans(self, ctx: commands.Context, memb: discord.Member = None):
        if memb is None:
            baza_info = Baza.get_member(ctx.author.id)

            embed = discord.Embed(
                title="💵 BILANS KONTA 💵",
                description=f"{ctx.author.mention}, twój bilans\n\n{baza_info[1]} CC.",
                color=discord.Color.dark_green()
            )

            embed.set_footer(text=str(ctx.author), icon_url=ctx.author.avatar_url)

            await ctx.send(embed=embed)
        else:
            baza_info = Baza.get_member(memb.id)
            embed = discord.Embed(
                title="💵 BILANS KONTA 💵",
                description=f"Bilans {memb.mention}\n\n{baza_info[1]} CC.",
                color=discord.Color.dark_green()
            )

            embed.set_footer(text=str(memb), icon_url=memb.avatar_url)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def add_money(self, ctx: commands.Context, member: discord.Member, amount: int):
        await ctx.send(f"Dano {amount}CC dla {member.mention}")
        Baza.update_money(member.id, amount)


def setup(bot):
    bot.add_cog(Coins(bot))
