import os

from teinfbot.db import db_session
from teinfbot.bot import TeinfBot
from teinfbot.paths import *

EXTENSIONS = []


def addExtensionDirectory(path, prefix):
    EXTS = [ext.split(".")[0] for ext in os.listdir(path) if ext.endswith(".py")]
    for ext in EXTS:
        EXTENSIONS.append(prefix + ext)


addExtensionDirectory(COGS_PATH, "teinfbot.cogs.")
addExtensionDirectory(COMMANDS_PATH, "teinfbot.commands.")
addExtensionDirectory(TASKS_PATH, "teinfbot.tasks.")

token = os.environ.get("ACCESS_TOKEN")

bot = TeinfBot(token, EXTENSIONS)
