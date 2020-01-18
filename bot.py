import os
import discord
from discord.ext import commands

prefix = "."
bot = commands.Bot(command_prefix=prefix)
client = discord.Client()


@bot.event
async def on_ready():
    print(
        f'\n\nZalogowano jako : {bot.user} - {bot.user.id}\nWersja: {discord.__version__}\n')
    # await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Aktywny!"))


# ładowanie rozszerzeń
def get_extensions(ext_dir, name: str):
    ext_folder = name  # folder w którym są rozszerzenia
    ext_path = os.path.join(ext_dir, ext_folder)
    ext_elems = os.listdir(ext_path)

    for ext in ext_elems:
        if ext[-3:] == ".py":
            yield name + "." + ext[:-3]


if __name__ == '__main__':
    for extension in get_extensions(os.getcwd(), 'cogs'):
        try:
            bot.load_extension(extension)
        except Exception as error:
            print(f'{extension} COULD NOT BE LOADED. [{error}]')
        else:
            print("LOADED " + extension)

access_token = os.environ["ACCESS_TOKEN"]
bot.run(access_token)
