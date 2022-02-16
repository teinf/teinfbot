import math

import discord
from discord.ext import commands
from discord_slash import SlashContext, cog_ext, SlashCommandOptionType
from discord_slash.utils import manage_commands

from teinfbot.bot import TeinfBot
from teinfbot.utils.guilds import guild_ids
from teinfbot.utils.music.YTDLSource import YTDLSource
from teinfbot.utils.music.song import Song
from teinfbot.utils.music.voice_state import VoiceState


class Music(commands.Cog):
    def __init__(self, bot: TeinfBot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, ctx: SlashContext):
        state = self.voice_states.get(ctx.guild.id)

        if not state:
            state = VoiceState(self.bot, ctx)
            self.voice_states[ctx.guild.id] = state

        return state

    def cog_unload(self):
        for state in self.voice_states.values():
            self.bot.loop.create_task(state.stop())

    async def cog_before_invoke(self, ctx: SlashContext):
        ctx.voice_state = self.get_voice_state(ctx)

    async def cog_command_error(self, ctx: SlashContext, error: commands.CommandError):
        await ctx.send('Nadarzył się problem: {}'.format(str(error)))

    def cog_check(self, ctx: commands.Context):
        if not ctx.guild:
            raise commands.NoPrivateMessage('Tej komendy nie można użyć w prywatnej wiadomości.')

        return True

    @cog_ext.cog_slash(name='join', description='Dołączam do kanału', guild_ids=guild_ids, options=[])
    async def _join(self, ctx: SlashContext):
        await self.ensure_voice_state(ctx)
        ctx.voice_state = self.get_voice_state(ctx)

        destination = ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()
        await ctx.send("Pomyślnie dołączyłem na kanał")

    @cog_ext.cog_slash(name='leave', description='Wychodzę z kanału', guild_ids=guild_ids, options=[])
    async def _leave(self, ctx: SlashContext):
        ctx.voice_state = self.get_voice_state(ctx)

        if not ctx.voice_state.voice:
            return await ctx.send('Nie jesteś połączony z żadnym kanałem')

        await ctx.voice_state.stop()
        del self.voice_states[ctx.guild.id]

        await ctx.send("Opuściłem kanał")

    @cog_ext.cog_slash(name='volume', description='Ustawia głośność', guild_ids=guild_ids, options=[
        manage_commands.create_option(
            name='volume',
            description='Wartość głośności',
            option_type=SlashCommandOptionType.INTEGER,
            required=True
        )
    ])
    async def _volume(self, ctx: SlashContext, volume: int):
        ctx.voice_state = self.get_voice_state(ctx)

        if not ctx.voice_state.is_playing:
            return await ctx.send('Nic nie gra w tym momencie')
        if 0 > volume > 100:
            return await ctx.send('Wartość musi zawierać się w przedziale 0-100')

        ctx.voice_state.volume = volume / 100

        await ctx.send(f'Głośność została zmieniona na {volume}%')

    @cog_ext.cog_slash(name='now', description='Pokazuje aktualnie graną piosenkę', guild_ids=guild_ids, options=[])
    async def _now(self, ctx: SlashContext):
        ctx.voice_state = self.get_voice_state(ctx)
        await ctx.send(embed=ctx.voice_state.current.create_embed())

    @cog_ext.cog_slash(name='pause', description='Pauzuje odtwarzacz', guild_ids=guild_ids, options=[])
    async def _pause(self, ctx: SlashContext):
        ctx.voice_state = self.get_voice_state(ctx)
        if ctx.voice_state.is_playing and ctx.voice_state.voice.is_playing():
            ctx.voice_state.voice.pause()

    @cog_ext.cog_slash(name='resume', description='Ponawiam odtwarzacz', guild_ids=guild_ids, options=[])
    async def _resume(self, ctx: SlashContext):
        ctx.voice_state = self.get_voice_state(ctx)
        if ctx.voice_state.is_playing and ctx.voice_state.voice.is_paused():
            ctx.voice_state.voice.resume()

    @cog_ext.cog_slash(name='stop', description='Zatrzymuje odtwarzacz i czyści kolejkę', guild_ids=guild_ids, options=[])
    async def _stop(self, ctx: SlashContext):
        ctx.voice_state = self.get_voice_state(ctx)

        ctx.voice_state.songs.clear()

        if ctx.voice_state.is_playing:
            ctx.voice_state.voice.stop()

    @cog_ext.cog_slash(name='skip', description='Pomija aktualnie graną muzykę', guild_ids=guild_ids, options=[])
    async def _skip(self, ctx: SlashContext):
        ctx.voice_state = self.get_voice_state(ctx)

        if not ctx.voice_state.is_playing:
            return await ctx.send('Nie gram żadnej muzyki w tym momencie')

        ctx.voice_state.skip()

    @cog_ext.cog_slash(name='queue', description='Pokazuje kolejkę', guild_ids=guild_ids, options=[
        manage_commands.create_option(
            name='strona',
            description='Podaj stronę kolejki',
            option_type=SlashCommandOptionType.INTEGER,
            required=False
        )
    ])
    async def _queue(self, ctx: SlashContext, page: int = 1):
        ctx.voice_state = self.get_voice_state(ctx)

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Kolejka jest pusta')

        items_per_page = 10
        pages = math.ceil(len(ctx.voice_state.songs) / items_per_page)

        start = (page - 1) * items_per_page
        end = items_per_page + start

        queue = ''

        for i, song in enumerate(ctx.voice_state.songs[start:end], start=start):
            queue += '`{0}.` [**{1.source.title}**](1.source.url)\n'.format(i + 1, song)

        embed = (discord.Embed(description='**{} utwory:**\n\n{}'.format(len(ctx.voice_state.songs), queue))
                 .set_footer(text='Strona {}/{}'.format(page, pages)))

        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name='remove', description='Usuwam utwór z kolejki', guild_ids=guild_ids, options=[
        manage_commands.create_option(
            name='indeks',
            description='indeks muzyki',
            option_type=SlashCommandOptionType.INTEGER,
            required=True
        )
    ])
    async def _remove(self, ctx: SlashContext, index: int):
        ctx.voice_state = self.get_voice_state(ctx)

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Kolejka jest pusta')

        ctx.voice_state.songs.remove(index - 1)

    @cog_ext.cog_slash(name='play', description='Odtwarza muzyke/dodaje do kolejki', guild_ids=guild_ids, options=[
        manage_commands.create_option(
            name='zrodlo',
            description='url/nazwa piosenki',
            option_type=SlashCommandOptionType.STRING,
            required=True
        )
    ])
    async def _play(self, ctx: SlashContext, zrodlo: str):
        await self.ensure_voice_state(ctx)
        ctx.voice_state = self.get_voice_state(ctx)

        if not ctx.voice_state.voice:
            await ctx.invoke(self._join)

        source = await YTDLSource.create_source(ctx, zrodlo, loop=self.bot.loop)

        song = Song(source)

        await ctx.voice_state.songs.put(song)
        await ctx.send('Zakolejkowano: {}'.format(str(source)))

    @staticmethod
    async def ensure_voice_state(ctx: SlashContext):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError('Nie jesteś połączony z kanałem')

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                raise commands.CommandError('Bot aktualnie jest na kanale')


def setup(bot: TeinfBot):
    bot.add_cog(Music(bot))