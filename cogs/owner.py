from discord.ext import commands
import discord
from typing import List
from enum import Enum


class Roles(Enum):
    OWNER = 423934002043289601
    H_ADMIN = 573208859590524949
    ADMIN = 486472082994233374
    MODERATOR = 423933999971565579


class Owner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Hidden - nie pokaże się w .help
    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def load_cog(self, ctx, *, cog: str):
        """Komenda ładująca cog.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUKCES!`**')

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def unload_cog(self, ctx, *, cog: str):
        """Komenda wyładująca cog.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUKCES!`**')

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def reload_cog(self, ctx, *, cog: str):
        """Komenda reładująca cog.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUKCES!`**')

    @commands.command(name='cleanbot', hidden=True)
    @commands.is_owner()
    # @commands.has_any_role(Roles.H_ADMIN, Roles.ADMIN)
    async def cleanbot(self, ctx, num: int = 15):
        deleted = await ctx.channel.purge(limit=num+1, check=lambda m: m.author == self.bot.user)
        msg = await ctx.channel.send(f"Usunięto {len(deleted)} wiadomości")
        await msg.delete(delay=10)
        await ctx.message.delete()

    @commands.command(name='clean', hidden=True)
    @commands.is_owner()
    # @commands.has_any_role(Roles.H_ADMIN, Roles.ADMIN)
    async def clean(self, ctx, num: int = 15):
        deleted = await ctx.channel.purge(limit=num+1)
        msg = await ctx.channel.send(f"Usunięto {len(deleted)} wiadomości")
        await msg.delete(delay=10)
        await ctx.message.delete()

    @commands.command(name='cleanciv', hidden=True)
    @commands.is_owner()
    # @commands.has_any_role(Roles.H_ADMIN, Roles.ADMIN)
    async def cleanciv(self, ctx, num: int = 15):
        deleted = await ctx.channel.purge(limit=num+1, check=lambda m: len(m.content) == 8 and m.content[3] == "-")
        msg = await ctx.channel.send(f"Usunięto {len(deleted)} wiadomości")
        await msg.delete(delay=10)
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(Owner(bot))
