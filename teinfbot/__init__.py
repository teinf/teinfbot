import os

from teinfbot.bot import TeinfBot
from teinfbot.paths import PATH_COGS

EXTENSIONS = [cog.split(".")[0] for cog in os.listdir(PATH_COGS) if cog.endswith(".py")]
EXT_PREFIX = "teinfbot.cogs."

EXTENSIONS = [EXT_PREFIX + ext for ext in EXTENSIONS]

database_url = os.environ.get("DATABASE_URL")

token = os.environ.get("ACCESS_TOKEN")
bot = TeinfBot(token, EXTENSIONS)


