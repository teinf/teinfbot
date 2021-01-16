import discord
from discord.ext import commands

from teinfbot.db import db_session
from teinfbot.paths import *


class TeinfBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=".",
            intents=discord.Intents.all(),
            reconnect=True,
        )

        self.guild_id = 406476256646004736

    def run(self):
        try:
            self.loop.run_until_complete(self.bot_start())
        except KeyboardInterrupt:
            self.loop.run_until_complete(self.bot_close())

    async def bot_start(self):
        self.retrieve_extensions()
        token = os.environ.get("ACCESS_TOKEN")
        await self.login(token)
        await self.connect()

    def retrieve_extensions(self):
        EXTENSIONS = []

        def addExtensionDirectory(path, prefix):
            EXTS = [ext.split(".")[0] for ext in os.listdir(path) if ext.endswith(".py")]
            for ext in EXTS:
                EXTENSIONS.append(prefix + ext)

        addExtensionDirectory(COGS_PATH, "teinfbot.cogs.")
        addExtensionDirectory(COMMANDS_PATH, "teinfbot.commands.")
        addExtensionDirectory(TASKS_PATH, "teinfbot.tasks.")

        for extension in EXTENSIONS:
            print(extension)
            try:
                self.load_extension(extension)
                print(f"[EXT] Success - {extension}")
            except commands.ExtensionNotFound:
                print(f"[EXT] Failed - {extension}")

    async def bot_close(self):
        await super().logout()
        db_session.close()

    async def on_ready(self):
        print(
            f'\nLogged as : {self.user} - {self.user.id}\nVersion: {discord.__version__}\n')
