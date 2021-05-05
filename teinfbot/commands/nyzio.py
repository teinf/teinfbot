import random
import string

from discord.ext import commands
from discord_slash import SlashContext, cog_ext

from teinfbot.bot import TeinfBot
from teinfbot.utils.guilds import guild_ids


class Nyzio(commands.Cog):
    def __init__(self, bot: TeinfBot):
        self.bot: TeinfBot = bot

    @cog_ext.cog_slash(name="nyzio", description="Nyzio", guild_ids=guild_ids)
    async def __nyzio(self, ctx: SlashContext):
        
        random_letter = random.choice(string.ascii_uppercase)
        await ctx.send(random_letter + "yzio")


def setup(bot: TeinfBot):
    bot.add_cog(Nyzio(bot))
