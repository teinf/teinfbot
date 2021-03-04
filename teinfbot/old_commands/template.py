from discord.ext import commands


@commands.command()
async def hello(ctx: commands.Context):
    await ctx.send('Hello {0.display_name}.'.format(ctx.author))


def setup(bot):
    bot.add_command(hello)
