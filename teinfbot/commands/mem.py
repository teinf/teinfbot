import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext, SlashCommandOptionType, cog_ext
from discord_slash.utils import manage_commands
from teinfbot.bot import TeinfBot
from teinfbot.utils.meme import Meme
from teinfbot.utils.guilds import guild_ids

class Mem(commands.Cog):
    def __init__(self, bot: TeinfBot):
        self.bot: TeinfBot = bot

    @cog_ext.cog_slash(name="mem", description="Wysyła losowego mema!" ,guild_ids=guild_ids)
    async def __mem(self, ctx: SlashContext):
        await ctx.ack(True)
        random_meme = await Meme.random_meme_async()

        await ctx.send(embed=random_meme.embed)

def setup(bot: TeinfBot):
    bot.add_cog(Mem(bot))