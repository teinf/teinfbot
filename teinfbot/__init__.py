import os

from teinfbot.db import db_session
from teinfbot.bot import TeinfBot
from teinfbot.paths import PATH_COGS
from teinfbot.paths import COMMANDS_PATH

EXTENSIONS = []

COGS = [cog.split(".")[0] for cog in os.listdir(PATH_COGS) if cog.endswith(".py")]
COGS_PREFIX = "teinfbot.cogs."
for cog in COGS:
    EXTENSIONS.append(COGS_PREFIX + cog)

COMMANDS = [command.split(".")[0] for command in os.listdir(COMMANDS_PATH) if command.endswith(".py")]
COMMANDS_PREFIX = "teinfbot.commands."
for command in COMMANDS:
    EXTENSIONS.append(COMMANDS_PREFIX + command)

token = os.environ.get("ACCESS_TOKEN")

bot = TeinfBot(token, EXTENSIONS)
