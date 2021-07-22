import discord
from discord.ext import commands
from discord_slash import SlashContext, SlashCommandOptionType, cog_ext
from discord_slash.utils import manage_commands

from teinfbot.bot import TeinfBot
from teinfbot.utils.guilds import guild_ids
from teinfbot.utils.music import MusicVideo

from youtube_dl import YoutubeDL
import io
import aiohttp

from typing import List


class Download(commands.Cog):

    def __init__(self, bot: TeinfBot):
        self.bot: TeinfBot = bot

    @cog_ext.cog_slash(name="download", description="Podaje link do pobrania", guild_ids=guild_ids, options=[
        manage_commands.create_option(
            name="url",
            description="Link do filmu",
            option_type=SlashCommandOptionType.STRING,
            required=True
        )
    ])
    async def __download(self, ctx: SlashContext, url: str):
        video = await MusicVideo.get(url)
        await ctx.send(content=str(video.source))


def setup(bot: TeinfBot):
    bot.add_cog(Download(bot))
