from typing import Optional

import discord
from discord import VoiceChannel, VoiceClient
from discord_slash import SlashContext

from teinfbot.bot import TeinfBot
from teinfbot.utils.music import QueueManager, MusicVideo
from teinfbot.utils.guilds import guild_ids


class MusicPlayer:
    FFMPEG_OPTS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    playing_now: Optional[MusicVideo] = None

    def __init__(self, bot: TeinfBot):
        self.bot = bot
        self.queue: QueueManager = QueueManager(bot)

    async def play(self, url: str, ctx: SlashContext) -> bool:
        music_video = await MusicVideo.get(url)
        if not music_video:
            return False

        self.queue.add(music_video)

        voice = self.get_voice()

        voice_channel = ctx.author.voice.channel
        if voice and voice.is_connected():
            await voice.move_to(voice_channel)
        else:
            voice = await voice_channel.connect()

        if not self.playing_now:
            # Brak kolejki
            voice.play(discord.FFmpegPCMAudio(music_video.source, **
            self.FFMPEG_OPTS), after=lambda x: self.play_next_song(ctx))
            self.playing_now = music_video

            em = discord.Embed(
                title="MUSIC BOT",
                description=f"Odtwarzam {music_video.title}\n{music_video.webpage}",
                color=discord.Colour.green()
            )
            em.set_image(url=music_video.thumbnail)
            await ctx.send(embed=em)

        else:
            # Kolejka
            em = discord.Embed(
                title="MUSIC BOT",
                description=f"Dodano {music_video.title} do kolejki\n{music_video.webpage}",
                color=discord.Colour.gold()
            )
            em.set_image(url=music_video.thumbnail)
            await ctx.send(embed=em)

    def play_next_song(self, ctx: SlashContext):
        next_song = self.queue.get_next()
        if not next_song:
            self.playing_now = None
            return

        voice = self.get_voice()
        voice.play(discord.FFmpegPCMAudio(next_song.source, **
        self.FFMPEG_OPTS), after=lambda x: self.play_next_song(ctx))
        self.playing_now = next_song

    async def pause(self) -> bool:
        voice = self.get_voice()
        if voice.is_playing():
            voice.pause()
            return True
        return False

    async def resume(self) -> bool:
        voice = self.get_voice()

        if not voice.is_playing():
            voice.resume()
            return True
        return False

    async def stop(self) -> bool:
        self.queue.clear()

        voice = self.get_voice()
        voice.stop()

        self.playing_now = None
        return True

    async def skip(self) -> bool:
        voice = self.get_voice()
        voice.stop()
        return True

    def get_voice(self) -> VoiceClient:
        voice: VoiceClient = discord.utils.get(
            self.bot.voice_clients, guild=self.bot.get_guild(guild_ids[0]))
        return voice
