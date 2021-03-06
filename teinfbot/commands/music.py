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


class Music(commands.Cog):
    def __init__(self, bot: TeinfBot):
        self.bot: TeinfBot = bot
        self.queue = List[MusicVideo]

    @cog_ext.cog_slash(name="music", description="Granie muzyki", guild_ids=guild_ids)
    async def __music(self, ctx: SlashContext):
        await ctx.ack(True)

    @cog_ext.cog_subcommand(base='music', name='play', guild_ids=guild_ids, options=[
        manage_commands.create_option(
            name="url",
            description="Link do muzyki",
            option_type=SlashCommandOptionType.STRING,
            required=True
        )
    ])
    async def __music_play(self, ctx: SlashContext, url: str):
        await ctx.ack(True)
        music_video = await MusicVideo.get(url)
        if not music_video:
            await ctx.send("Niepoprawny link lub zła strona")
            return
        

        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        channel = ctx.author.voice.channel
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        voice.play(discord.FFmpegPCMAudio(music_video.source, **FFMPEG_OPTS))

    @cog_ext.cog_subcommand(base='music', name='pause', guild_ids=guild_ids)
    async def __music_pause(self, ctx: SlashContext):
        await ctx.ack(True)
        voice: discord.VoiceClient = discord.utils.get(
            self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()

    @cog_ext.cog_subcommand(base='music', name='resume', guild_ids=guild_ids)
    async def __music_resume(self, ctx: SlashContext):
        await ctx.ack(True)
        voice: discord.VoiceClient = discord.utils.get(
            self.bot.voice_clients, guild=ctx.guild)
        if not voice.is_playing():
            voice.resume()

    @cog_ext.cog_subcommand(base='music', name='stop', guild_ids=guild_ids)
    async def __music_stop(self, ctx: SlashContext):
        await ctx.ack(True)
        voice: discord.VoiceClient = discord.utils.get(
            self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.stop()


def setup(bot: TeinfBot):
    bot.add_cog(Music(bot))
