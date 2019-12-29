import os
import discord
from discord.ext import commands
from discord.ext.commands import Bot

currentDirectory = os.getcwd()

prefix = "."
bot = commands.Bot(command_prefix=prefix)

@bot.event
async def on_ready():
    print(
        f'\n\nZalogowano jako : {bot.user} - {bot.user.id}\nWersja: {discord.__version__}\n')
    # await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Aktywny!"))


@bot.event
async def on_message(message):
    # sprawdzanie czy wiadomosc jest komendą
    await bot.process_commands(message)


# ładowanie rozszerzeń
extensionsPlaceName = 'cogs'  # folder w którym są rozszerzenia
extensionsPath = os.path.join(currentDirectory, extensionsPlaceName)
extensionsElements = os.listdir(extensionsPath)
extensions = []
for extension in extensionsElements:
    if extension[-3:] == ".py":
        extensions.append(extensionsPlaceName + "." + extension[:-3])

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as error:
            print(f'{extension} COULD NOT BE LOADED. [{error}]')
        else:
            print("LOADED " + extension)

access_token= os.environ["ACCESS_TOKEN"]
bot.run(access_token)
