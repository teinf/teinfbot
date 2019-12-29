import os
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import random

currentDirectory = os.getcwd()

prefix = "."  # tutaj wpisujesz prefix
bot = commands.Bot(command_prefix=prefix)

logChannelID = 660770250001874944
welcomeChannelID = 497043785071722496


@bot.event
async def on_ready():
    print(
        f'\n\nZalogowano jako : {bot.user} - {bot.user.id}\nWersja: {discord.__version__}\n')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Aktywny!"))
    logsChannel = bot.get_channel(logChannelID)


@bot.event
async def on_message(message):
    # wysyłanie wiadomości do konsoli
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")

    # wysyłanie wiadomosci do logów
    if message.channel.id != logChannelID and message.author.id != bot.user.id:
        msgEm = discord.Embed(
            title=f"{message.author}", description=f"Wiadomość: {message.content}", colour=discord.Color.green())
        msgEm.set_footer(text=f'{message.channel}, ID: {message.author.id}')
        logsChannel = bot.get_channel(logChannelID)
        await logsChannel.send(embed=msgEm)

    # sprawdzanie czy wiadomosc jest komendą
    await bot.process_commands(message)


@bot.event
async def on_message_delete(message):
    # wysyłanie do konsoli
    print(
        f"USUNIĘTO: {message.channel}: {message.author}: {message.author.name}: {message.content}")

    # wysyłanie wiadomosci do logów
    if message.channel.id != logChannelID and message.author.id != bot.user.id:
        msgEm = discord.Embed(
            title=f"USUNIĘTO: {message.author}", description=f"Wiadomość: {message.content}", colour=discord.Color.red())
        msgEm.set_footer(text=f'{message.channel}, ID: {message.author.id}')
        logsChannel = bot.get_channel(logChannelID)
        await logsChannel.send(embed=msgEm)
        

extensionPlace = 'cogs'  # folder w którym są rozszerzenia
extensionNames = ['games', 'interaktywne', 'kasyno', 'moderacja',
                  'narzędzia', 'owner', 'zabawa', 'serverStats']  # nazwy rozszerzen
extensions = [extensionPlace + "." + extension for extension in extensionNames]

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as error:
            print(f'{extension} nie mozna załadować. [{error}]')

access_token= os.environ["ACCESS_TOKEN"]
bot.run(access_token)
