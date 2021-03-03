import os

import discord
from discord.ext import commands
from discord_slash import SlashContext, SlashCommandOptionType, cog_ext
from discord_slash.utils import manage_commands
from gtts import gTTS

from teinfbot.bot import TeinfBot
from teinfbot.paths import ASSETS_PATH
from teinfbot.utils.guilds import guild_ids


class Say(commands.Cog):
    def __init__(self, bot: TeinfBot):
        self.bot: TeinfBot = bot

    @cog_ext.cog_slash(name="say", guild_ids=guild_ids, options=[
        manage_commands.create_option(
            name="lang",
            description="Język mówienia",
            option_type=SlashCommandOptionType.STRING,
            # choices=[{"name": value, "value": key} for key, value in langs._langs.items()],
            choices=[
                {
                    'name': 'Afrykański',
                    'value': 'af'
                },
                {
                    'name': 'Arabski',
                    'value': 'ar'
                },
                {
                    'name': 'Czeski',
                    'value': 'ch'
                },
                {
                    'name': 'Niemiecki',
                    'value': 'de'
                },
                {
                    'name': 'Angielski',
                    'value': 'en'
                },
                {
                    'name': 'Grecki',
                    'value': 'el'
                },
                {
                    'name': 'Hiszpański',
                    'value': 'es'
                },
                {
                    'name': 'Francuzki',
                    'value': 'fr'
                },
                {
                    'name': 'Hindi',
                    'value': 'hi'
                },
                {
                    'name': 'Włoski',
                    'value': 'it'
                },
                {
                    'name': 'Khmer',
                    'value': 'km'
                },
                {
                    'name': 'Koreanśki',
                    'value': 'ko'
                },
                {
                    'name': 'Łaciński',
                    'value': 'la'
                },
                {
                    'name': 'Norweski',
                    'value': 'no'
                },
                {
                    'name': 'Polski',
                    'value': 'pl'
                },
                {
                    'name': 'Rosyjski',
                    'value': 'ru'
                },
                {
                    'name': 'Słowacki',
                    'value': 'sk'
                },
                {
                    'name': 'Albanian',
                    'value': 'sq'
                },
                {
                    'name': 'Szwedzki',
                    'value': 'sv'
                },
                {
                    'name': 'Turecki',
                    'value': 'tr'
                },
                {
                    'name': 'Ukraiński',
                    'value': 'uk'
                },
                {
                    'name': 'Arabski',
                    'value': 'af'
                },
                {
                    'name': 'Thai',
                    'value': 'th'
                },
                {
                    'name': 'Wietnamski',
                    'value': 'vi'
                },
                {
                    'name': 'Chiński',
                    'value': 'zh-CN'
                }
            ],
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
        await ctx.ack(True)

        TTS_FILE_NAME = 'music.mp3'
        TTS_FILE_PATH = os.path.join(ASSETS_PATH, 'gtts', TTS_FILE_NAME)

        tts = gTTS(message, lang=lang)
        with open(TTS_FILE_PATH, 'wb') as f:
            tts.write_to_fp(f)

        await ctx.send(file=discord.File(TTS_FILE_PATH))


def setup(bot: TeinfBot):
    bot.add_cog(Say(bot))
