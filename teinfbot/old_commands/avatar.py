import discord
from discord.ext import commands


@commands.command()
async def avatar(ctx: commands.Context, member: discord.Member = None):
    """ Wyświetla link z obrazem użtykownika @nick
    jeśli nie podamy użytkownika, to wywołamy na sobie """

    await ctx.message.delete()

    member = member or ctx.message.author
    await ctx.send(f"{member.avatar_url}")


def setup(bot):
    bot.add_command(avatar)
