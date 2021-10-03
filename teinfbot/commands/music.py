import discord
from discord.ext import commands
from discord_slash import SlashContext, SlashCommandOptionType, cog_ext
from discord_slash.utils import manage_commands

from teinfbot.bot import TeinfBot
from teinfbot.utils.guilds import guild_ids
from teinfbot.utils.music import MusicPlayer


class Music(commands.Cog):

    music_player: MusicPlayer = None

    def __init__(self, bot: TeinfBot):
        self.bot: TeinfBot = bot
        self.music_player = MusicPlayer(bot)

    @cog_ext.cog_slash(name="music", description="Granie muzyki", guild_ids=guild_ids)
    async def __music(self, ctx: SlashContext):
        pass

    @cog_ext.cog_subcommand(base='music', name='play', description="Włącza podaną piosenkę", guild_ids=guild_ids, options=[
        manage_commands.create_option(
            name="url",
            description="Link do muzyki",
            option_type=SlashCommandOptionType.STRING,
            required=True
        )
    ])
    async def __music_play(self, ctx: SlashContext, url: str):
        await self.music_player.play(url, ctx)

    @cog_ext.cog_subcommand(base='music', name='now', description="Pokazuje obecnie graną piosenkę", guild_ids=guild_ids)
    async def __music_now(self, ctx: SlashContext):
        music_video = self.music_player.playing_now
        em = discord.Embed(
            title="MUSIC BOT",
            description=f"Obecnie gram {music_video.title}\n{music_video.webpage}",
            color=discord.Colour.dark_green()
        )
        em.set_thumbnail(url=music_video.thumbnail)
        await ctx.send(embed=em)

    @cog_ext.cog_subcommand(base='music', name='pause', description="Pauzuje piosenkę", guild_ids=guild_ids)
    async def __music_pause(self, ctx: SlashContext):
        await self.music_player.pause()
        await ctx.send("Zapauzowano", hidden=True)

    @cog_ext.cog_subcommand(base='music', name='resume', description="Wznawia piosenkę", guild_ids=guild_ids)
    async def __music_resume(self, ctx: SlashContext):
        await self.music_player.resume()
        await ctx.send("Wznowiono", hidden=True)

    @cog_ext.cog_subcommand(base='music', name='stop', description="Wyłącza granie piosenek", guild_ids=guild_ids)
    async def __music_stop(self, ctx: SlashContext):
        await self.music_player.stop()
        await ctx.send("Zastopowano", hidden=True)

    @cog_ext.cog_subcommand(base='music', name='skip', description="Przechodzi do następnego utworu", guild_ids=guild_ids)
    async def __music_skip(self, ctx: SlashContext):
        await self.music_player.skip()
        await ctx.send("Skipnięto", hidden=True)

    @cog_ext.cog_subcommand(base='music', name='clear', description="Czyści kolejkę grania", guild_ids=guild_ids)
    async def __music_clear(self, ctx: SlashContext):
        await self.music_player.queue.clear()
        await ctx.send("Wyczyszczono playlistę", hidden=True)


def setup(bot: TeinfBot):
    bot.add_cog(Music(bot))