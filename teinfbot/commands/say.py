import os

import discord
from discord.ext import commands
from discord_slash import SlashContext, SlashCommandOptionType, cog_ext
from discord_slash.utils import manage_commands
from gtts import gTTS

from teinfbot.bot import TeinfBot
from teinfbot.utils.paths import ASSETS_PATH
from teinfbot.utils.guilds import guild_ids
import asyncio

import json


class Say(commands.Cog):
    def __init__(self, bot: TeinfBot):
        self.bot: TeinfBot = bot

    @cog_ext.cog_slash(name="say", guild_ids=guild_ids, description="Mówi daną wiadomość w podanym języku", options=[
        manage_commands.create_option(
            name="lang",
            description="Język mówienia",
            option_type=SlashCommandOptionType.STRING,
            # choices=[{"name": value, "value": key} for key, value in langs._langs.items()],
            choices=json.loads(open(os.path.join(ASSETS_PATH, 'gtts', 'languages.json'), 'r').read()),
            required=True
        ),
        manage_commands.create_option(
            name="message",
            description="Wiadomość",
            option_type=SlashCommandOptionType.STRING,
            required=True
        )
    ])
    async def __say(self, ctx: SlashContext, lang: str, message: str):
        

        if len(message) <= 1:
            return
            
        TTS_FILE_NAME = 'translated_message.mp3'
        TTS_FILE_PATH = os.path.join(ASSETS_PATH, 'gtts', TTS_FILE_NAME)

        tts = gTTS(message, lang=lang)
        with open(TTS_FILE_PATH, 'wb') as f:
            tts.write_to_fp(f)

        if ctx.author.voice:
            channel: discord.VoiceChannel = ctx.author.voice.channel
            voice: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                voice = await channel.connect()

            
            voice.play(discord.FFmpegPCMAudio(source=TTS_FILE_PATH))

            while voice.is_playing():
                await asyncio.sleep(0.1)

            await voice.disconnect()
        else:
            await ctx.send(file=discord.File(TTS_FILE_PATH))
        

        




def setup(bot: TeinfBot):
    bot.add_cog(Say(bot))
