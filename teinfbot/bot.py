import colorama
import discord
from discord.ext import commands
from discord_slash import SlashCommand

from teinfbot.db import db_session
from teinfbot.paths import *


class TeinfBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=".",
            intents=discord.Intents.all(),
            reconnect=True,
        )

    def run(self):
        try:
            self.loop.run_until_complete(self.bot_start())
        except KeyboardInterrupt:
            self.loop.run_until_complete(self.bot_close())

    async def bot_start(self):
        slash = SlashCommand(self, override_type=True, sync_commands=True)
        self.retrieve_extensions()
        token = os.environ.get("ACCESS_TOKEN")
        await self.login(token)
        await self.connect()

    def retrieve_extensions(self):
        def addExtension(path, prefix):
            EXTS = [ext.split(".")[0] for ext in os.listdir(path) if ext.endswith(".py")]
            print(colorama.Fore.BLUE + "\n" + f"=== LOADING {prefix.upper()} ===" + "\n")
            for ext in EXTS:
                try:
                    ext_fullname = "teinfbot." + prefix + "." + ext
                    self.load_extension(ext_fullname)
                    print(f"{colorama.Fore.GREEN}[{prefix.upper()}] Success - {ext}")
                except commands.ExtensionNotFound:
                    print(f"{colorama.Fore.RED}[{prefix.upper()}] Failed - {ext}")

            print(colorama.Style.RESET_ALL)

        addExtension(COGS_PATH, "cogs")
        addExtension(COMMANDS_PATH, "commands")
        addExtension(TASKS_PATH, "tasks")
        addExtension(EVENTS_PATH, "events")

        print(colorama.Style.RESET_ALL)

    async def bot_close(self):
        await super().logout()
        db_session.close()

    async def on_ready(self):
        print(
            f'\nLogged as : {self.user} - {self.user.id}\nVersion: {discord.__version__}\n')
