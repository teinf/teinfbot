import os

from discord.ext import commands

from teinfbot import TeinfBot
from teinfbot.paths import PATH_COGS


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
            extensions = [cog.split(".")[0] for cog in os.listdir(PATH_COGS) if cog.endswith(".py")]
            for extension in extensions:
                await self.reload_extension(ctx, extension)


def setup(bot):
    bot.add_cog(Owner(bot))
