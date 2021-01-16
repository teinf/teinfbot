from discord.ext import commands
import discord
import os

from gtts import gTTS

from teinfbot.paths import PATH_ASSETS

@commands.command()
async def say(ctx, language, *textToSay):
    """ Użycie: .say en Hello There """
    await ctx.message.delete()

    TTS_FILE_NAME = 'music.mp3'
    TTS_FILE_PATH = os.path.join(PATH_ASSETS, 'gtts', TTS_FILE_NAME)

    textToSay = " ".join(textToSay)

    tts = gTTS(textToSay, lang=language)
    with open(TTS_FILE_PATH, 'wb') as f:
        tts.write_to_fp(f)

    await ctx.send(file=discord.File(TTS_FILE_PATH))


def setup(bot):
    bot.add_command(say)
