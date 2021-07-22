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

    queue: List[MusicVideo] = []
    FFMPEG_OPTS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    def __init__(self, bot: TeinfBot):
        self.bot: TeinfBot = bot

    @cog_ext.cog_slash(name="music", description="Granie muzyki", guild_ids=guild_ids)
    async def __music(self, ctx: SlashContext):
        pass

    @classmethod
    def clear_queue(cls):
        cls.queue = []

    @classmethod
    def play_next_song(cls, voice: discord.VoiceClient):

        if len(cls.queue) > 0:
            cls.queue.pop(0)

        if len(cls.queue) > 0:
            voice.play(discord.FFmpegPCMAudio(
                cls.queue[0].source, **cls.FFMPEG_OPTS), after=lambda x: cls.play_next_song(voice))

    @cog_ext.cog_subcommand(base='music', name='play', description="Włącza podaną piosenkę", guild_ids=guild_ids, options=[
        manage_commands.create_option(
            name="url",
            description="Link do muzyki",
            option_type=SlashCommandOptionType.STRING,
            required=True
        )
    ])
    async def __music_play(self, ctx: SlashContext, url: str):

        music_video = await MusicVideo.get(url)
        if not music_video:
            await ctx.send("Niepoprawny link lub zła strona", hidden=True)
            return

        if len(self.queue) >= 1:
            self.queue.append(music_video)
            em = discord.Embed(
                title="MUSIC BOT",
                description=f"Dodano {music_video.title} do kolejki\n{music_video.webpage}",
                color=discord.Colour.gold()
            )
            em.set_image(url=music_video.thumbnail)
            await ctx.send(embed=em)
            return

        elif len(self.queue) == 0:
            em = discord.Embed(
                title="MUSIC BOT",
                description=f"Odtwarzam {music_video.title}\n{music_video.webpage}",
                color=discord.Colour.green()
            )
            em.set_image(url=music_video.thumbnail)
            await ctx.send(embed=em)
            self.queue.append(music_video)

        voice: discord.VoiceClient = discord.utils.get(
            self.bot.voice_clients, guild=ctx.guild)

        channel = ctx.author.voice.channel
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        voice.play(discord.FFmpegPCMAudio(music_video.source, **
                   self.FFMPEG_OPTS), after=lambda x: self.play_next_song(voice))

    @cog_ext.cog_subcommand(base='music', name='pause', description="Pauzuje piosenkę", guild_ids=guild_ids)
    async def __music_pause(self, ctx: SlashContext):

        voice: discord.VoiceClient = discord.utils.get(
            self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()

        await ctx.send("Zapauzowano", hidden=True)

    @cog_ext.cog_subcommand(base='music', name='resume', description="Wznawia piosenkę", guild_ids=guild_ids)
    async def __music_resume(self, ctx: SlashContext):

        voice: discord.VoiceClient = discord.utils.get(
            self.bot.voice_clients, guild=ctx.guild)
        if not voice.is_playing():
            voice.resume()

        await ctx.send("Wznowiono", hidden=True)

    @cog_ext.cog_subcommand(base='music', name='stop', description="Wyłącza granie piosenek", guild_ids=guild_ids)
    async def __music_stop(self, ctx: SlashContext):

        voice: discord.VoiceClient = discord.utils.get(
            self.bot.voice_clients, guild=ctx.guild)
        self.clear_queue()
        voice.stop()

        await ctx.send("Zastopowano", hidden=True)

    @cog_ext.cog_subcommand(base='music', name='skip', description="Przechodzi do następnego utworu", guild_ids=guild_ids)
    async def __music_skip(self, ctx: SlashContext):

        voice: discord.VoiceClient = discord.utils.get(
            self.bot.voice_clients, guild=ctx.guild)
        voice.stop()

        await ctx.send("Skipnięto", hidden=True)

    @cog_ext.cog_subcommand(base='music', name='clear', description="Czyści kolejkę grania", guild_ids=guild_ids)
    async def __music_clear(self, ctx: SlashContext):

        voice: discord.VoiceClient = discord.utils.get(
            self.bot.voice_clients, guild=ctx.guild)
        self.clear_queue()
        await ctx.send("Wyczyszczono playlistę", hidden=True)


def setup(bot: TeinfBot):
    bot.add_cog(Music(bot))
